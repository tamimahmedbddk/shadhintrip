document.addEventListener('DOMContentLoaded', function() {
    const url = window.location.pathname;
    const tourTab = document.querySelector('.tabs__button[data-tab-target=".-tab-item-1"]');
    const visaTab = document.querySelector('.tabs__button[data-tab-target=".-tab-item-2"]');
    const flightTab = document.querySelector('.tabs__button[data-tab-target=".-tab-item-3"]');
    const hotelTab = document.querySelector('.tabs__button[data-tab-target=".-tab-item-4"]');

    const tabs = [tourTab, visaTab, flightTab, hotelTab];

    // Function to deactivate all tabs
    const deactivateTabs = () => {
        tabs.forEach(tab => tab.classList.remove('is-tab-el-active'));
    };

    // Activate the correct tab based on the URL
    if (url.includes('/tour')) {
        deactivateTabs();
        tourTab.classList.add('is-tab-el-active');
    } else if (url.includes('/visa')) {
        deactivateTabs();
        visaTab.classList.add('is-tab-el-active');
    } else if (url.includes('/flight')) {
        deactivateTabs();
        flightTab.classList.add('is-tab-el-active');
    } else if (url.includes('/hotel')) {
        deactivateTabs();
        hotelTab.classList.add('is-tab-el-active');
    }

    // Existing logic to populate dropdowns and setup event listeners
    const countryDropdown = document.querySelector('[data-x="tour-country"] .searchFormItemDropdown__list');
    const categoryDropdown = document.querySelector('[data-x="tour-type"] .searchFormItemDropdown__list');
    const packageDropdown = document.querySelector('[data-x="tour-package"] .searchFormItemDropdown__list');
    const visaCountryDropdown = document.querySelector('[data-x="visa-country"] .searchFormItemDropdown__list');
    const visaTypeDropdown = document.querySelector('[data-x="visa-type"] .searchFormItemDropdown__list');
    const visaPackageDropdown = document.querySelector('[data-x="visa-package"] .searchFormItemDropdown__list');
    const searchButton = document.getElementById('search-button');
    const selectedTourSlugInput = document.getElementById('selected-tour-slug');
    const visaSearchButton = document.getElementById('visa-search-button');
    const selectedVisaSlugInput = document.getElementById('selected-visa-slug');

    const fetchJson = (url) => {
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            });
    };

    const populateDropdown = (dropdownElement, data, valueKey, textKey, iconKey = null, imageKey = null) => {
        dropdownElement.innerHTML = '';
        data.forEach(item => {
            const option = document.createElement('div');
            option.classList.add('searchFormItemDropdown__item', 'search-country-image');
            option.innerHTML = `
                <button class="js-select-control-button" data-value="${item[valueKey]}" data-slug="${item.slug || ''}" data-country-id="${item.country_id || ''}">
                    <span class="js-select-control-choice">${item[textKey]}</span>
                    ${iconKey ? `<span>${item[iconKey]}</span>` : ''}
                    ${imageKey ? `<img src="${item[imageKey]}" alt="logo icon">` : ''}
                </button>`;
            dropdownElement.appendChild(option);
        });
        setupDropdownListeners();
    };

    const debounce = (func, delay) => {
        let debounceTimer;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(context, args), delay);
        };
    };

    const populateTourCountries = () => {
        fetchJson('/get_tour_countries/')
            .then(data => {
                populateDropdown(countryDropdown, data, 'id', 'name', null, 'image');
            })
            .catch(error => {
                console.error('Error fetching tour countries:', error);
            });
    };

    const populateTourCategories = (countryId) => {
        const categoryChosen = document.querySelector('[data-x="tour-type"] .js-select-control-chosen');
        if (categoryChosen) {
            categoryChosen.innerText = 'Loading...';
        }
        fetchJson(`/get_tour_categories/?country_id=${countryId}`)
            .then(data => {
                populateDropdown(categoryDropdown, data, 'category_id', 'category_name', 'category_icon');
                categoryDropdown.dataset.countryId = countryId;
                if (categoryChosen) {
                    categoryChosen.innerText = 'Search Tour Type';
                }
            })
            .catch(error => {
                console.error('Error fetching tour categories:', error);
            });
    };

    const populateTourPackages = (countryId, categoryId) => {
        const packageChosen = document.querySelector('[data-x="tour-package"] .js-select-control-chosen');
        if (packageChosen) {
            packageChosen.innerText = 'Loading...';
        }
        fetchJson(`/get_tour_packages/?country_id=${countryId}&category_id=${categoryId}`)
            .then(data => {
                populateDropdown(packageDropdown, data, 'id', 'title', null, 'image');
                if (packageChosen) {
                    packageChosen.innerText = 'Search Tour Package';
                }
            })
            .catch(error => {
                console.error('Error fetching tour packages:', error);
            });
    };

    const populateVisaCountries = () => {
        fetchJson('/get_visa_countries/')
            .then(data => {
                populateDropdown(visaCountryDropdown, data, 'id', 'name', null, 'image');
            })
            .catch(error => {
                console.error('Error fetching visa countries:', error);
            });
    };

    const populateVisaTypes = (countryId) => {
        const visaTypeChosen = document.querySelector('[data-x="visa-type"] .js-select-control-chosen');
        if (visaTypeChosen) {
            visaTypeChosen.innerText = 'Loading...';
        }
        fetchJson(`/get_visa_types/?country_id=${countryId}`)
            .then(data => {
                populateDropdown(visaTypeDropdown, data, 'id', 'name', null, 'image');
                visaTypeDropdown.dataset.countryId = countryId;
                if (visaTypeChosen) {
                    visaTypeChosen.innerText = 'Search Visa Type';
                }
            })
            .catch(error => {
                console.error('Error fetching visa types:', error);
            });
    };

    const populateVisaPackages = (countryId, visaTypeId) => {
        const visaPackageChosen = document.querySelector('[data-x="visa-package"] .js-select-control-chosen');
        if (visaPackageChosen) {
            visaPackageChosen.innerText = 'Loading...';
        }
        fetchJson(`/get_visa_packages/?country_id=${countryId}&visa_type_id=${visaTypeId}`)
            .then(data => {
                populateDropdown(visaPackageDropdown, data, 'id', 'title', null, 'image');
                if (visaPackageChosen) {
                    visaPackageChosen.innerText = 'Search Visa Package';
                }
            })
            .catch(error => {
                console.error('Error fetching visa packages:', error);
            });
    };

    const setupDropdownListeners = () => {
        document.querySelectorAll('.js-select-control-button').forEach(button => {
            button.addEventListener('click', debounce(function() {
                const value = this.dataset.value;
                const slug = this.dataset.slug;
                const parentDropdown = this.closest('.searchFormItemDropdown');
                const chosenElement = parentDropdown.previousElementSibling.querySelector('.js-select-control-chosen');

                if (chosenElement) {
                    chosenElement.innerText = this.querySelector('.js-select-control-choice').innerText;
                    chosenElement.dataset.value = value;
                    if (parentDropdown.dataset.x === 'tour-country') {
                        chosenElement.dataset.countryId = value;
                    } else if (parentDropdown.dataset.x === 'visa-country') {
                        chosenElement.dataset.countryId = value;
                    }
                } else {
                    console.error('Chosen element not found');
                }

                if (parentDropdown.dataset.x === 'tour-country') {
                    console.log(`Country selected: ${value}`);
                    populateTourCategories(value);
                } else if (parentDropdown.dataset.x === 'tour-type') {
                    console.log(`Type selected: ${value}`);
                    const countryId = categoryDropdown.dataset.countryId;
                    if (countryId) {
                        console.log(`countryChosen: ${countryId}`);
                        populateTourPackages(countryId, value);
                    } else {
                        alert('Please select a country first.');
                    }
                } else if (parentDropdown.dataset.x === 'tour-package') {
                    if (slug) {
                        selectedTourSlugInput.value = slug;
                        searchButton.href = `/tours/tour-details/${slug}/`;
                    } else {
                        console.error('Tour slug not found');
                    }
                } else if (parentDropdown.dataset.x === 'visa-country') {
                    console.log(`Country selected: ${value}`);
                    populateVisaTypes(value);
                } else if (parentDropdown.dataset.x === 'visa-type') {
                    console.log(`Type selected: ${value}`);
                    const countryId = visaTypeDropdown.dataset.countryId;
                    if (countryId) {
                        console.log(`countryChosen: ${countryId}`);
                        populateVisaPackages(countryId, value);
                    } else {
                        alert('Please select a country first.');
                    }
                } else if (parentDropdown.dataset.x === 'visa-package') {
                    if (slug) {
                        selectedVisaSlugInput.value = slug;
                        visaSearchButton.href = `/visa/visa-details/${slug}/`;
                    } else {
                        console.error('Visa slug not found');
                    }
                }

                parentDropdown.classList.remove('is-active'); // Close the dropdown
            }, 300));
        });
    };

    populateTourCountries();
    populateVisaCountries();
});
