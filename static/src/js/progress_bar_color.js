odoo.define('Task_tracker.progress_bar_color', function (require) {
"use strict";

var core = require('web.core');
var utils = require('web.utils');
var FieldProgressBar = require('web.basic_fields').FieldProgressBar


FieldProgressBar.include({
    _render_value: function(event){
            this._super.apply(this, arguments)

            if (this.model === "task") {
                let value = this.value;
                let maxValue = this.max_value;
                let barComplete;
                if (value <= maxValue) {
                   barComplete = value/maxValue * 100;
                } else {
                   barComplete = 100;
                }
                this.$('.o_progressbar_complete').toggleClass('o_progress_red',barComplete>0 && barComplete<=99).css('width',`${barComplete}%`);
                this.$('.o_progressbar_complete').toggleClass('o_progress_green',barComplete==100).css('width',barComplete + '%');
                if (this.readonly) {
                    if (maxValue !== 100) {
                        this.$('.o_progressbar_value').text(utils.human_number(value) + " / " + utils.human_number(maxValue));
                    } else {
                        this.$('.o_progressbar_value').text(utils.human_number(value) + "%");
                    }
                }
            }


    },
});
});


