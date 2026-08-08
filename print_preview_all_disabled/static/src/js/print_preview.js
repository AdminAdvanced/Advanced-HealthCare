/** @odoo-module **/

import { Component, onMounted, useRef } from "@odoo/owl";
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

        onMounted(() => {
            if (this.pdfFrame.el) {
                this.pdfFrame.el.src = this.props.pdfUrl;
            }
        });
    }

    /**
     * Print the PDF currently displayed in the iframe.
     */
    onPrint() {
        const iframe = this.pdfFrame.el;

        if (!iframe) {
            console.error("PDF iframe was not found.");
            return;
        }

        try {
            iframe.contentWindow.focus();
            iframe.contentWindow.print();
        } catch (error) {
            console.error("Could not print PDF:", error);
        }
    }

    /**
     * Download the PDF using Odoo's standard report download endpoint.
     */
    async onDownload() {
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

    /*
     * Generate the normal Odoo PDF URL.
     */
    const pdfUrl = getReportUrl(
        action,
        "pdf",
        action.context || {}
    );

    console.log("PDF URL:", pdfUrl);

    /*
     * Same endpoint used by Odoo's standard downloadReport().
     */
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

    /*
     * Open the preview popup.
     */
    env.services.dialog.add(
        PrintPreviewDialog,
        {
            pdfUrl: pdfUrl,
            downloadUrl: downloadUrl,
            downloadData: downloadData,
        }
    );

    /*
     * Prevent Odoo from executing its normal
     * downloadReport() afterwards.
     */
    return true;
}


registry
    .category("ir.actions.report handlers")
    .add(
        "print_preview_all",
        printPreviewReportHandler
    );