/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";
import { ListController } from "@web/views/list/list_controller";
import { FormController } from "@web/views/form/form_controller";


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


// ============================================================
// LIST VIEW
// ============================================================

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);

        this.orm = useService("orm");
        this.deleteRestricted = false;

        onWillStart(async () => {
            const model = this.props.resModel;

            this.deleteRestricted = await checkDeleteRestriction(
                this.orm,
                model
            );

        });
    },

    getStaticActionMenuItems() {
        const items = super.getStaticActionMenuItems(...arguments);

        const model = this.props.resModel;
        const activeActions = this.archInfo?.activeActions;

        if (items.delete && this.deleteRestricted) {
            items.delete.isAvailable = () => false;
        }

        return items;
    },
});


// ============================================================
// FORM VIEW
// ============================================================

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);

        this.orm = useService("orm");
        this.deleteRestricted = false;

        onWillStart(async () => {
            const model = this.props.resModel;

            this.deleteRestricted = await checkDeleteRestriction(
                this.orm,
                model
            );

        });
    },

    getStaticActionMenuItems() {
        const items = super.getStaticActionMenuItems(...arguments);

        const model = this.props.resModel;
        const activeActions = this.archInfo?.activeActions;

        if (items.delete && this.deleteRestricted) {
            items.delete.isAvailable = () => false;
        }

        return items;
    },
});