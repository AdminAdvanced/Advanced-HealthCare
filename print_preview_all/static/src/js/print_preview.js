```javascript
/** @odoo-module **/

import { Component, onMounted, useRef } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { getReportUrl } from "@web/webclient/actions/reports/utils";
import { download } from "@web/core/network/download";


export class PrintPreviewDialog extends Component {
    static template = "print_preview_all.PrintPreviewDialog";

    static components = {
        Dialog,
    };

    static props = {
        close: Function,
        pdfUrl: String,
        downloadUrl: String,
        downloadData: Object,
        title: { type: String, optional: true },
    };

    setup() {
        this.pdfFrame = useRef("pdfFrame");

        onMounted(() => {
            if (this.pdfFrame.el) {
                this.pdfFrame.el.src = this.props.pdfUrl;
            }
        });
    }

    onPrint() {
        const iframe = this.pdfFrame.el;

        if (!iframe) {
            return;
        }

        try {
            iframe.contentWindow.focus();
            iframe.contentWindow.print();
        } catch (error) {
            console.error(
                "Could not print PDF from preview:",
                error
            );
        }
    }

    async onDownload() {
        await download({
            url: this.props.downloadUrl,
            data: this.props.downloadData,
        });
    }
}


async function printPreviewReportHandler(action, options, env) {

    // Only intercept PDF reports
    if (action.report_type !== "qweb-pdf") {
        return false;
    }

    /*
     * Build the PDF URL.
     *
     * We use action.context here because the report action
     * already contains the relevant context.
     */
    const reportContext = action.context || {};

    const pdfUrl = getReportUrl(
        action,
        "pdf",
        reportContext
    );

    /*
     * This is the same endpoint used by Odoo's
     * standard report download.
     */
    const downloadUrl = "/report/download";

    const downloadData = {
        data: JSON.stringify([
            pdfUrl,
            action.report_type,
        ]),
        context: JSON.stringify(reportContext),
    };

    /*
     * Open the PDF preview dialog.
     */
    env.services.dialog.add(
        PrintPreviewDialog,
        {
            pdfUrl: pdfUrl,
            downloadUrl: downloadUrl,
            downloadData: downloadData,
            title:
                action.display_name ||
                action.name ||
                "Print Preview",
        }
    );

    /*
     * Tell Odoo that our handler handled the report.
     *
     * This prevents the normal downloadReport()
     * from running.
     */
    return true;
}


registry
    .category("ir.actions.report handlers")
    .add(
        "print_preview_all",
        printPreviewReportHandler
    );
```
