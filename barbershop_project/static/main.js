document.addEventListener('DOMContentLoaded', function() {
    const masterSelect = document.getElementById('id_master');
    const servicesSelect = document.getElementById('id_services');

    function loadServices(masterId) {
        if (masterId) {
            fetch(`/api/services/?master_id=${masterId}`)
                .then(response => response.json())
                .then(data => {
                    servicesSelect.innerHTML = '';
                    data.services.forEach(service => {
                        const option = document.createElement('option');
                        option.value = service.id;
                        option.textContent = service.name;
                        servicesSelect.appendChild(option);
                    });
                });
        }
    }

    if (masterSelect && servicesSelect) {
        // Загружаем услуги при изменении мастера
        masterSelect.addEventListener('change', function() {
            loadServices(this.value);
        });

        // Загружаем услуги при ошибке валидации
        if (masterSelect.value) {
            loadServices(masterSelect.value);
        }
    }
});