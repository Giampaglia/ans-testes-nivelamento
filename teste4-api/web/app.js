new Vue({
    el: '#app',
    data: {
        busca: '',
        resultados: [],
        carregando: false
    },
    methods: {
        buscar() {
            if (this.busca.length < 2) return;
            
            this.carregando = true;
            this.resultados = [];
            
            axios.get('http://localhost:8000/operadoras/', {
                params: {
                    nome: this.busca,
                    limite: 20
                }
            })
            .then(response => {
                this.resultados = response.data;
            })
            .catch(error => {
                console.error("Erro na busca:", error);
                alert(error.response?.data?.detail || "Erro ao buscar operadoras");
            })
            .finally(() => {
                this.carregando = false;
            });
        }
    }
});