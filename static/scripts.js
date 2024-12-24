document.addEventListener('DOMContentLoaded', () => {
    const trainSection = document.getElementById('train-section');
    const predictSection = document.getElementById('predict-section');

    const toggleSection = (sectionToShow) => {
        trainSection.classList.add('hidden');
        predictSection.classList.add('hidden');
        sectionToShow.classList.remove('hidden');
    };

    document.getElementById('toggle-train').addEventListener('click', () => {
        toggleSection(trainSection);
    });

    document.getElementById('toggle-predict').addEventListener('click', () => {
        toggleSection(predictSection);
    });

    initTrainForm();
    initPredictForm();
});

function showModal(message) {
    const modal = document.getElementById('modal');
    const modalMessage = document.getElementById('modal-message');
    if (modal && modalMessage) {
        modalMessage.textContent = message;
        modal.style.display = 'block';

        const closeButton = document.querySelector('.close');
        closeButton.onclick = () => {
            modal.style.display = 'none';
        };

        window.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };
    } else {
        console.error("Modal elements not found");
    }
}

function initTrainForm() {
    document.getElementById('train-form')?.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);

        try {
            const response = await fetch('/upload-train', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                showModal('Файл успешно загружен для обучения!');
            } else {
                const error = await response.json();
                showModal(`Ошибка: ${error.error}`);
            }
        } catch (error) {
            showModal(`Ошибка подключения: ${error.message}`);
        }
    });
}

function initPredictForm() {
    document.getElementById('predict-form')?.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const downloadChecked = document.getElementById('download').checked;
        formData.append('download', downloadChecked);

        try {
            const response = await fetch('/upload-predict', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                if (downloadChecked) {
                    const blob = await response.blob();
                    const link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = 'processed_file';
                    link.click();
                    showModal('Файл успешно обработан и загружен!');
                } else {
                    showModal('Файл успешно обработан!');
                }
            } else {
                const error = await response.json();
                showModal(`Ошибка: ${error.error}`);
            }
        } catch (error) {
            showModal(`Ошибка подключения: ${error.message}`);
        }
    });
}
