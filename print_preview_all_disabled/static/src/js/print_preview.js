/** @odoo-module **/

import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { getReportUrl } from "@web/webclient/actions/reports/utils";
import { download } from "@web/core/network/download";


class PrintPreviewDialog extends Component {
    static template = "print_preview_all.PrintPreviewDialog";

    static components = {
        Dialog,
    };

    static props = {
        close: Function,
        pdfUrl: String,
        downloadUrl: String,
        downloadData: Object,
    };

    setup() {
        this.pdfFrame = useRef("pdfFrame");

        this.state = useState({
            loading: true,
            error: false,
        });

        onMounted(() => {
            if (this.pdfFrame.el) {
                this.pdfFrame.el.src = this.props.pdfUrl;
            }
        });
    }

    onPdfLoaded() {
        console.log("PDF loaded successfully");

        this.state.loading = false;
        this.state.error = false;
    }

    onPdfError() {
        console.error("Failed to load PDF");

        this.state.loading = false;
        this.state.error = true;
    }

    onPrint() {
        const iframe = this.pdfFrame.el;

        if (!iframe || this.state.loading || this.state.error) {
            return;
        }

        try {
            iframe.contentWindow.focus();
            iframe.contentWindow.print();
        } catch (error) {
            console.error("Could not print PDF:", error);
        }
    }

    async onDownload() {
        if (this.state.loading || this.state.error) {
            return;
        }

        try {
            await download({
                url: this.props.downloadUrl,
                data: this.props.downloadData,
            });
        } catch (error) {
            console.error("Could not download PDF:", error);
        }
    }
}


async function printPreviewReportHandler(action, options, env) {

    console.log("PRINT PREVIEW HANDLER:", action);

    if (action.report_type !== "qweb-pdf") {
        return false;
    }

    const pdfUrl = getReportUrl(
        action,
        "pdf",
        action.context || {}
    );

    console.log("PDF URL:", pdfUrl);

    const downloadUrl = "/report/download";

    const downloadData = {
        data: JSON.stringify([
            pdfUrl,
            action.report_type,
        ]),
        context: JSON.stringify(
            action.context || {}
        ),
    };

    env.services.dialog.add(
        PrintPreviewDialog,
        {
            pdfUrl: pdfUrl,
            downloadUrl: downloadUrl,
            downloadData: downloadData,
        }
    );

    return true;
}


registry
    .category("ir.actions.report handlers")
    .add(
        "print_preview_all",
        printPreviewReportHandler
    );