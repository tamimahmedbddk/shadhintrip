document.addEventListener('DOMContentLoaded', function() {
    const countryDropdown = document.querySelector('[data-x="tour-country"] .searchFormItemDropdown__list');
    const categoryDropdown = document.querySelector('[data-x="tour-type"] .searchFormItemDropdown__list');
    const packageDropdown = document.querySelector('[data-x="tour-package"] .searchFormItemDropdown__list');
    const searchButton = document.getElementById('search-button');
    const selectedTourSlugInput = document.getElementById('selected-tour-slug');

    const fetchJson = (url) => {
        console.log(`Fetching JSON from: ${url}`);
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            });
    };

    const populateDropdown = (dropdownElement, data, valueKey, textKey, imageKey) => {
        dropdownElement.innerHTML = '';
        data.forEach(item => {
            const option = document.createElement('div');
            option.classList.add('searchFormItemDropdown__item', 'search-country-image');
            option.innerHTML = `
                <button class="js-select-control-button" data-value="${item[valueKey]}" data-slug="${item.slug || ''}" data-country-id="${item.country_id || ''}">
                    <span class="js-select-control-choice">${item[textKey]}</span>
                    ${imageKey ? `<img src="${item[imageKey]}" alt="logo icon">` : ''}
                </button>`;
            dropdownElement.appendChild(option);
        });
        setupDropdownListeners();
    };

    const populateTourCountries = () => {
        fetchJson('/get_tour_countries/')
            .then(data => {
                populateDropdown(countryDropdown, data, 'id', 'name', 'image');
            })
            .catch(error => {
                console.error('Error fetching tour countries:', error);
            });
    };

    const populateTourCategories = (countryId) => {
        fetchJson(`/get_tour_categories/?country_id=${countryId}`)
            .then(data => {
                populateDropdown(categoryDropdown, data, 'category_id', 'name', null);
            })
            .catch(error => {
                console.error('Error fetching tour categories:', error);
            });
    };

    const populateTourPackages = (countryId, categoryId) => {
        console.log(`Country ID: ${countryId}, Category ID: ${categoryId}`); // Debugging line
        fetchJson(`/get_tour_packages/?country_id=${countryId}&category_id=${categoryId}`)
            .then(data => {
                populateDropdown(packageDropdown, data, 'id', 'title', 'image');
                console.log('Tour packages fetched successfully'); // Debugging line
            })
            .catch(error => {
                console.error('Error fetching tour packages:', error);
            });
    };

    const setupDropdownListeners = () => {
        document.querySelectorAll('.js-select-control-button').forEach(button => {
            button.addEventListener('click', function() {
                const value = this.dataset.value;
                const slug = this.dataset.slug; // Get the slug
                const parentDropdown = this.closest('.searchFormItemDropdown');
                const chosenElement = parentDropdown.previousElementSibling.querySelector('.js-select-control-chosen');

                if (chosenElement) {
                    chosenElement.innerText = this.querySelector('.js-select-control-choice').innerText;
                    chosenElement.dataset.value = value;
                    if (parentDropdown.dataset.x === 'tour-country') {
                        chosenElement.dataset.countryId = value; // Set the country ID on country selection
                    }
                } else {
                    console.error('Chosen element not found');
                }

                if (parentDropdown.dataset.x === 'tour-country') {
                    console.log(`Country selected: ${value}`);
                    populateTourCategories(value);
                    const categoryChosen = document.querySelector('[data-x="tour-type"] .js-select-control-chosen');
                    if (categoryChosen) {
                        categoryChosen.innerText = 'Search Tour Type';
                        categoryChosen.dataset.value = '';
                    }
                    const packageChosen = document.querySelector('[data-x="tour-package"] .js-select-control-chosen');
                    if (packageChosen) {
                        packageChosen.innerText = 'Search Tour Package';
                        packageChosen.dataset.value = '';
                    }
                } else if (parentDropdown.dataset.x === 'tour-type') {
                    console.log(`Category selected: ${value}`);
                    const countryChosen = document.querySelector('[data-x="tour-country"] .js-select-control-chosen');
                    if (countryChosen && countryChosen.dataset.value) {
                        const countryId = countryChosen.dataset.value;
                        console.log(`countryChosen: ${countryChosen.innerText}, countryChosen.dataset.value: ${countryChosen.dataset.value}`);
                        populateTourPackages(countryId, value);
                    } else {
                        console.error('Country ID not found');
                    }
                } else if (parentDropdown.dataset.x === 'tour-package') {
                    if (slug) {
                        selectedTourSlugInput.value = slug;
                        searchButton.href = `/tours/tour-details/${slug}/`; // Update the URL
                    } else {
                        console.error('Tour slug not found');
                    }
                }
            });
        });
    };

    // Initial load
    populateTourCountries();
});
