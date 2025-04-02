new Vue({
  el: "#app",
  data: {
      busca: "",
      resultados: [],
      carregando: false
  },
  methods: {
      async buscar() {
          if (!this.busca) return alert("Digite um termo para buscar.");

          this.carregando = true;

          try {
              const response = await axios.get(`http://127.0.0.1:8000/operadoras/`, {
                  params: { termo: this.busca, limite: 5 }
              });

              this.resultados = response.data;
          } catch (error) {
              console.error("Erro na busca:", error);
              this.resultados = [];
          } finally {
              this.carregando = false;
          }
      }
  }
});
