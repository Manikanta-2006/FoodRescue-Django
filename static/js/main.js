/**
 * FoodRescue Platform Frontend Scripts
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto-dismiss Bootstrap alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {
                alert.style.display = 'none';
            }
        }, 6000);
    });

    // 2. Dynamic live search / API test helper
    const searchInput = document.getElementById('liveDonationSearch');
    const searchResults = document.getElementById('liveSearchResults');

    if (searchInput && searchResults) {
        let debounceTimer;
        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            const query = this.value.trim();
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
                return;
            }

            debounceTimer = setTimeout(function () {
                fetch(`/api/donations/?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        searchResults.innerHTML = '';
                        if (data.donations && data.donations.length > 0) {
                            searchResults.style.display = 'block';
                            data.donations.forEach(item => {
                                const row = document.createElement('a');
                                row.href = item.detail_url;
                                row.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center py-2';
                                row.innerHTML = `
                                    <div>
                                        <strong class="text-success">${item.food_name}</strong>
                                        <div class="small text-muted">${item.quantity} ${item.unit} &bull; ${item.city}</div>
                                    </div>
                                    <span class="badge bg-light text-dark">${item.category}</span>
                                `;
                                searchResults.appendChild(row);
                            });
                        } else {
                            searchResults.style.display = 'block';
                            searchResults.innerHTML = '<div class="list-group-item text-muted small py-2">No active matching donations found.</div>';
                        }
                    })
                    .catch(err => console.error("API error:", err));
            }, 300);
        });

        // Hide live search results when clicking outside
        document.addEventListener('click', function (e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }

    // 3. Conditional Role selection handling in registration
    const roleSelect = document.getElementById('id_role');
    const orgGroup = document.getElementById('div_id_organization_name');
    if (roleSelect && orgGroup) {
        function toggleOrgField() {
            if (roleSelect.value === 'NGO') {
                orgGroup.style.display = 'block';
            } else {
                orgGroup.style.display = 'block'; // Keep visible but note optional
            }
        }
        roleSelect.addEventListener('change', toggleOrgField);
        toggleOrgField();
    }
});
