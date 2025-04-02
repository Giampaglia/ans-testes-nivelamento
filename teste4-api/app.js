new Vue({
    el: "#app",
    data: {
      busca: "",
      resultados: [],
      carregando: false
    },
    methods: {
        async buscar() {
            if (!this.busca.trim()) return;
            
            this.carregando = true;
            this.resultados = [];
          
            try {
              const response = await axios.get(`http://127.0.0.1:8000/operadoras/`, {
                params: { nome: this.busca, limite: 5 }
              });
          
              this.resultados = response.data;
            } catch (error) {
              console.error("Erro ao buscar operadoras:", error);
              alert("Erro ao buscar operadoras.");
            } finally {
              this.carregando = false;
            }
          }
          
    }
  });
  