/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";
import { ListController } from "@web/views/list/list_controller";
import { FormController } from "@web/views/form/form_controller";


/**
 * ============================================================
 * Draft configuration
 * ============================================================
 */

const DRAFT_STATES = {
    "sale.order": ["draft", "sent"],
    "purchase.order": ["draft", "sent"],
    "account.move": ["draft"],
    "account.payment": ["draft"],
    "stock.picking": ["draft"],
    "account.asset": ["draft"],
};


/**
 * ============================================================
 * Check whether a record is Draft
 * ============================================================
 */

function isDraftRecord(record, model) {
    if (!record || !model) {
        return false;
    }

    const allowedStates = DRAFT_STATES[model];

    if (!allowedStates) {
        return false;
    }

    const state = record.data?.state;

    return allowedStates.includes(state);
}


/**
 * ============================================================
 * Check delete restriction
 * ============================================================
 */

async function checkDeleteRestriction(orm, model) {
    if (!model) {
        return false;
    }

    try {
        return await orm.call(
            "res.users",
            "check_user_delete_restriction",
            [model]
        );
    } catch (error) {
        console.error(
            "DELETE CONTROL: failed to check restriction",
            model,
            error
        );

        return false;
    }
}


/**
 * ============================================================
 * LIST VIEW
 * ============================================================
 */

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);

        this.orm = useService("orm");
        this.deleteRestricted = false;

        onWillStart(async () => {
            const model = this.props.resModel;

            this.deleteRestricted =
                await checkDeleteRestriction(
                    this.orm,
                    model
                );
        });
    },

    getStaticActionMenuItems() {
        const items = super.getStaticActionMenuItems(...arguments);

        const model = this.props.resModel;

        if (items.delete && this.deleteRestricted) {

            items.delete.isAvailable = () => {

                const root = this.model?.root;

                if (!root) {
                    return false;
                }

                const selection = root.selection || [];

                if (!selection.length) {
                    return false;
                }

                /*
                 * If ALL selected records are Draft,
                 * allow Delete.
                 */

                const allDraft = selection.every(
                    record => isDraftRecord(record, model)
                );

                if (allDraft) {
                    return true;
                }

                /*
                 * At least one non-Draft record exists.
                 * Delete remains restricted.
                 */

                return false;
            };
        }

        return items;
    },
});


/**
 * ============================================================
 * FORM VIEW
 * ============================================================
 */

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);

        this.orm = useService("orm");
        this.deleteRestricted = false;

        onWillStart(async () => {
            const model = this.props.resModel;

            this.deleteRestricted =
                await checkDeleteRestriction(
                    this.orm,
                    model
                );
        });
    },

    getStaticActionMenuItems() {
        const items = super.getStaticActionMenuItems(...arguments);

        const model = this.props.resModel;

        if (items.delete && this.deleteRestricted) {

            items.delete.isAvailable = () => {

                const record = this.model?.root;

                if (!record) {
                    return false;
                }

                /*
                 * Draft records can always be deleted.
                 */

                if (isDraftRecord(record, model)) {
                    return true;
                }

                /*
                 * Non-Draft restricted record.
                 */

                return false;
            };
        }

        return items;
    },
});