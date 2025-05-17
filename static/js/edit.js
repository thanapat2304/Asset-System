document.addEventListener("DOMContentLoaded", function() {
    const submitButton = document.querySelector('button[type="submit"]');
    submitButton.addEventListener('click', function(event) {
        const now = new Date();
        const thailandTime = new Intl.DateTimeFormat('en-GB', {
            timeZone: 'Asia/Bangkok',
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        }).format(now);

        const [date, time] = thailandTime.split(', ');
        const [day, month, year] = date.split('/');
        const formattedTime = `${year}-${month}-${day} ${time}`;

        document.getElementById('AS_Save_Time').value = formattedTime;
        document.getElementById('display_AS_Save_Time').textContent = formattedTime;
    });

    const asDateInput = document.querySelector('input[name="AS_Date"]');
    const yrInput = document.getElementById('YR');

    function updateYear() {
        const dateValue = asDateInput.value;
        if (dateValue) {
            yrInput.value = new Date(dateValue).getFullYear();
        }
    }

    asDateInput.addEventListener('change', updateYear);
    updateYear();
});

function formatNumber(input) {
    let value = input.value.replace(/,/g, '');
    
    let decimalIndex = value.indexOf('.');
    
    if (!isNaN(value) && decimalIndex === -1) {
        input.value = Number(value).toLocaleString('en-US');
    } else if (decimalIndex !== -1) {
        let beforeDecimal = value.substring(0, decimalIndex);
        let afterDecimal = value.substring(decimalIndex + 1, decimalIndex + 3);

        input.value = beforeDecimal.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + '.' + afterDecimal;
    }
}

function removeCommasBeforeSubmit(input) {
    input.value = input.value.replace(/,/g, '');
}

document.querySelector('.custom-select-trigger').addEventListener('click', function() {
    const options = document.querySelector('.custom-select-options');
    const select = document.querySelector('.custom-select');
    
    if (options.style.display === 'block') {
        options.style.display = 'none';
        select.classList.remove('open');
    } else {
        options.style.display = 'block';
        select.classList.add('open');
    }
});

document.querySelectorAll('.status-option').forEach(option => {
    option.addEventListener('click', function() {
        const selectedStatus = this.getAttribute('data-status');
        const lightColor = this.querySelector('.status-light').classList[1];

        document.getElementById('status-input').value = selectedStatus;

        const trigger = document.querySelector('.custom-select-trigger .selected-option');
        trigger.innerHTML = `<span class="status-light ${lightColor}"></span> ${this.innerText}`;

        document.querySelector('.custom-select-options').style.display = 'none';
    });
});