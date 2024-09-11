/** @odoo-module **/
import { Component } from "@odoo/owl";
import { useState } from "@odoo/owl";
import Chart from 'chart.js/auto';

export class Dashboard extends Component {
    setup() {
        this.state = useState({
            upcomingDeliveries: [],
            dailyPayments: [],
        });

        this.fetchData();
    }

    async fetchData() {
        const deliveries = await this._rpc({
            model: 'sale.order',
            method: 'get_upcoming_deliveries',
        });
        this.state.upcomingDeliveries = deliveries;

        const payments = await this._rpc({
            model: 'account.payment',
            method: 'get_daily_payments',
        });
        this.state.dailyPayments = payments;

        this.renderChart();
    }

    renderChart() {
        const ctx = document.getElementById('daily_payments_chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: this.state.dailyPayments.dates,
                datasets: [{
                    label: 'Payments Collected',
                    data: this.state.dailyPayments.amounts,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}
