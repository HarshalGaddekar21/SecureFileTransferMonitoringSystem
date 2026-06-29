/* =====================================================
   Secure File Transfer Monitoring System
   Dashboard JavaScript
   Version 2.0
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

    console.log("Secure File Transfer Monitoring System Loaded");

    // ==========================================
    // Search by File Name
    // ==========================================

    const searchInput = document.getElementById("searchInput");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            const value = this.value.toLowerCase();

            const rows = document.querySelectorAll("#eventTable tbody tr");

            rows.forEach(function (row) {

                const fileName = row.cells[3].innerText.toLowerCase();

                row.style.display = fileName.includes(value) ? "" : "none";

            });

        });

    }

    // ==========================================
    // Filter by Event Type
    // ==========================================

    const eventFilter = document.getElementById("eventFilter");

    if (eventFilter) {

        eventFilter.addEventListener("change", function () {

            const value = this.value.toLowerCase();

            const rows = document.querySelectorAll("#eventTable tbody tr");

            rows.forEach(function (row) {

                const eventType = row.cells[2].innerText.toLowerCase();

                if (value === "" || eventType.includes(value)) {

                    row.style.display = "";

                } else {

                    row.style.display = "none";

                }

            });

        });

    }

    // ==========================================
    // Refresh Dashboard
    // ==========================================

    const refreshBtn = document.getElementById("refreshBtn");

    if (refreshBtn) {

        refreshBtn.addEventListener("click", function () {

            location.reload();

        });

    }

    // ==========================================
    // Export Button
    // ==========================================

    const exportBtn = document.getElementById("exportBtn");

    if (exportBtn) {

        exportBtn.addEventListener("click", function () {

            window.location.href = "/reports";

        });

    }

    // ==========================================
    // Highlight Table Rows
    // ==========================================

    const tableRows = document.querySelectorAll("#eventTable tbody tr");

    tableRows.forEach(function (row) {

        row.addEventListener("mouseenter", function () {

            this.style.cursor = "pointer";

        });

    });

    // ==========================================
    // Show Current Date & Time
    // ==========================================

    const clockElement = document.getElementById("liveClock");

    if (clockElement) {

        function updateClock() {

            const now = new Date();

            clockElement.innerHTML =
                now.toLocaleDateString() +
                " | " +
                now.toLocaleTimeString();

        }

        updateClock();

        setInterval(updateClock, 1000);

    }

    console.log("Dashboard JavaScript Initialized");

});
