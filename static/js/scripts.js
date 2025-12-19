function atualizarRodape() {
    const agora = new Date();
    const data = agora.toLocaleDateString('pt-BR');
    const hora = agora.toLocaleTimeString('pt-BR');
    document.getElementById('data-hora-rodape').innerHTML = 
        `<strong>${data}</strong> | ${hora}`;
}
setInterval(atualizarRodape, 1000);
atualizarRodape();


document.getElementById('add-more').addEventListener('click', function() {
    const container = document.getElementById('items-container');
    const forms = container.querySelectorAll('.item-form');
    const lastForm = forms[forms.length - 1];
    const newForm = lastForm.cloneNode(true);
    newForm.querySelectorAll('input, select').forEach(input => {
        if (input.type !== 'hidden' && !input.name.includes('DELETE')) {
            if (input.tagName === 'SELECT') {
                input.selectedIndex = 0;
            } else {
                input.value = '';
                }
            }
            });
    container.appendChild(newForm);
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    totalForms.value = parseInt(totalForms.value) + 1;
        });
