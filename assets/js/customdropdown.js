const dropdownButton = document.getElementById('dropdown-button')
const dropdownOptions = document.getElementById('dropdown-options')
const dropdownSelected = document.getElementById('dropdown-selected')
const selectedCategoryInput = document.getElementById('selected-category')

dropdownButton.addEventListener('click', (e) => {
    e.stopPropagation()
    dropdownOptions.classList.toggle('hidden')
})

dropdownOptions.querySelectorAll('li').forEach((item) => {
    item.addEventListener('click', (e) => {
        e.stopPropagation()
        const value = item.getAttribute('data-value')
        dropdownSelected.textContent = value
        selectedCategoryInput.value = value

        // Optional: Highlight the selected item
        dropdownOptions.querySelectorAll('li').forEach((li) => li.classList.remove('bg-gray-100', 'font-semibold'))
        item.classList.add('bg-gray-100', 'font-semibold')

        dropdownOptions.classList.add('hidden')
    })
})

// Optional: Close dropdown if clicked outside
document.addEventListener('click', (e) => {
    if (!dropdownButton.contains(e.target) && !dropdownOptions.contains(e.target)) {
        dropdownOptions.classList.add('hidden')
    }
})