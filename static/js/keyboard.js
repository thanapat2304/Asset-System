function validateNumber(event) {
    if (event.key === " " || event.keyCode === 32) {
        event.preventDefault();
    }

    const value = event.target.value;
    event.target.value = value.replace(/[^0-9]/g, '');
}

function preventSpace(event) {
    if (event.key === " " || event.keyCode === 32) {
      event.preventDefault();
    }
}

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

function AMTNumber(event) {
    const value = event.target.value;
    event.target.value = value.replace(/[^0-9.,]/g, '');
}