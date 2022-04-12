odoo.define('helpdesk_api.dashboard', function (require) {
"use strict";
var AbstractAction = require('web.AbstractAction');
var view_registry = require('web.view_registry');
var ajax = require('web.ajax');
var core = require('web.core');
var QWeb = core.qweb;

var PosDashboard = AbstractAction.extend({
    template: 'Dashboard',

    events:{
        "click .widget-1": function(){ 
            var self = this;
            this.show_my_tickets(self);
            },
        
        "click .widget-2": function(){ 
            var self = this;
            this.show_customer_centered_tickets(self);
            },

        "click widget-3": function(){ 
            var self = this;
            this.show_issue_centered_tickets(self);
            },

        "click .widget-4": function(){ 
            var self = this;
            this.show_closed_tickets(self);
            },

        "click .widget-5": function(){ 
            var self = this;
            this.show_opened_tickets(self);
            },

        "click .widget-6": function(){ 
            var self = this;
            this.show_solved_tickets(self);
            },

        "click .widget-7": function(self){ 
            var self = this;
            this.show_unassigned_tickets(self);
            },

        "click .widget-8": function(){ 
            var self = this;
            this.show_failed_sla_tickets(self);
            },
        "click .widget-9": function(){ 
            var self = this;
            this.show_assigned_tickets(self);
            },

        },

    init: function(parent, context){
        this._super(parent, context);
        this.dashboards_templates = ['Dashboard'];
        this.today_sale = [];
        this.create_user_ticket = [];
        this._get_customer_centered_tickets = [];
        this._get_issue_other_centered_tickets = [];
        this._get_closed_tickets = [];
        this._get_opened_tickets = [];
        this._get_my_tickets_tickets = [];
        this._get_solved_tickets = [];
        this._get_unassigned_tickets = [];
        this._get_failed_sla_tickets = [];
        this._get_urgent_priority_tickets = [];
        this._get_high_priority_tickets = [];
    },
    willStart: function() {
        var self = this;
        return $.when(ajax.loadLibs(this), this._super()).then(function() {
            console.log(self.fetch_data())
            return self.fetch_data();
        });
    },

    start: function(){
        console.log("Start");
        var self = this;
        this.set("title", "Dashboard");
        return this._super().then(function(){
            self.render_dashboards();
             

        })
    },

    fetch_data: function() {
        var self = this;
        var def1 =  this._rpc({
                model: 'helpdeskticket.model',
                method: 'get_dashboard_details'
        }).then(function(result) {
            console.log("RES", result)
           self.create_user_ticket = result['create_user_ticket'],
           self._get_customer_centered_tickets = result['_get_customer_centered_tickets']
           self._get_issue_other_centered_tickets = result['_get_issue_other_centered_tickets']
           self._get_closed_tickets = result['_get_closed_tickets']
           self._get_opened_tickets = result['_get_opened_tickets']
           self._get_my_tickets_tickets = result['_get_my_tickets_tickets']
           self._get_solved_tickets = result['_get_solved_tickets']
           self._get_unassigned_tickets = result['_get_unassigned_tickets']
           self._get_failed_sla_tickets = result['_get_failed_sla_tickets']
           self._get_high_priority_tickets = result['_get_high_priority_tickets']
           self._get_urgent_priority_tickets = result['_get_urgent_priority_tickets']
        });
 
       
        return $.when(def1);
    },

    render_dashboards: function(){
        var self = this;
        _.each(this.dashboards_templates, function(template){
            self.$('.o_opos_dashboard').append(QWeb.render(template, {widget: self}));
        });
        
    },

    show_my_ticketszz: function(){
        var self = this;
        // e.preventDefault(); // prevents browser from reloading
        // var $action = $(e.currentTarget);
        // var action_ref = $action.attr('name');
        // console.log('ACTION CLICKED IS', action_ref)
        // var title = $action.attr('title');
        // var search_view_ref = $action.attr('search_view_ref');
        // if ($action.attr('name').includes("helpdesk_api.")) {
            this._rpc({
                model: 'helpdeskticket.model',
                method: 'create_action',
                args: ["one"],
            }).then(function (result) {

                if (result) {
                    self.do_action(result);
                }else{
                    console.log("Nothing to do")
                }
            });
        // }else{
        //     console.log("ATTRIBUTE NAME DOES NOT CONTAIN HELPDESK API")
        // }
            
    },

    show_my_tickets: function(e){
        var self = this;
        self.onDashboardActionClickedTickets('My tickets', 'helpdesk_api.helpdesk_my_ticket_action', 'helpdesk_api.helpdeskticket_model_view_search')
    },
    
    show_customer_centered_tickets: function(e){
        var self = this;
        self.onDashboardActionClickedTickets('Customer Centered tickets', 'helpdesk_api.helpdesk_customer_centered_ticket_action', 'helpdesk_api.helpdeskticket_model_view_search')

    },
    show_issue_centered_tickets: function(e){
        var self = this;
        self.onDashboardActionClickedTickets('Issue Centered tickets', 'helpdesk_api.helpdesk_issue_centered_ticket_action', 'helpdesk_api.helpdeskticket_model_view_search')
    },
    show_closed_tickets: function(e){
        var self = this;
        self.onDashboardActionClickedTickets('Closed tickets', 'helpdesk_api.helpdesk_closed_ticket_action', 'helpdesk_api.helpdeskticket_model_view_search')
    },

    show_opened_tickets: function(e){
        var self = this;
        self.onDashboardActionClickedTickets('Opened tickets', 'helpdesk_api.helpdesk_opened_ticket_action', 'helpdesk_api.helpdeskticket_model_view_search')
    },

    show_solved_tickets: function(e){
        var self = this;
        self.onDashboardActionClickedTickets('Solved tickets', 'helpdesk_api.helpdesk_solved_ticket_action', 'helpdesk_api.helpdeskticket_model_view_search')
    },

    show_unassigned_tickets: function(e){
        var self = this;
        self.onDashboardActionClickedTickets('Unassigned tickets', 'helpdesk_api.helpdesk_unassigned_ticket_action', 'helpdesk_api.helpdeskticket_model_view_search')
    },

    show_failed_sla_tickets: function(e){
        var self = this;
        self.onDashboardActionClickedTickets('Failed SLA tickets', 'helpdesk_api.helpdesk_failed_sla_ticket_action', 'helpdesk_api.helpdeskticket_model_view_search')
    },
    show_assigned_tickets: function(e){
        var self = this;
        self.onDashboardActionClickedTickets('Assigned', 'helpdesk_api.helpdesk_assigned_ticket_action', 'helpdesk_api.helpdeskticket_model_view_search')
    },

    onDashboardActionClickedTickets: function (title,action_ref,search_view_ref) {
        var self = this;
            this._rpc({
                model: 'helpdeskticket.model',
                method: 'create_action',
                args: [action_ref,title, search_view_ref] 
                // "helpdesk_api.helpdeskticket_model_view_search"],
            }).then(function (result) {
                if (result.action) {
                    self.do_action(result.action);
                }
            });
    },

})
core.action_registry.add('custom_dashboard_tag', PosDashboard);
return PosDashboard;
});
