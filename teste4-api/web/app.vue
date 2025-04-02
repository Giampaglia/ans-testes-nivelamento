<script setup>
import { ref } from 'vue';

const nomeOperadora = ref('');
const resultados = ref([]);
const carregando = ref(false);

const buscarOperadoras = async () => {
  carregando.value = true;

  try {
    const response = await fetch(`http://127.0.0.1:8000/operadoras/?nome=${nomeOperadora.value}&limite=5`);
    
    if (!response.ok) throw new Error('Erro ao buscar operadoras');

    const data = await response.json();
    console.log("Resposta da API:", data);  // 🔥 Debug: Veja os campos retornados

    resultados.value = data;
  } catch (error) {
    console.error(error);
    resultados.value = [];
  } finally {
    carregando.value = false;
  }
};

</script>

<template>
  <div>
    <h1>Busca de Operadoras de Saúde</h1>
    <input v-model="nomeOperadora" placeholder="Digite o nome da operadora ou Registro ANS..." />
    <button @click="buscarOperadoras">Buscar</button>
    
    <p v-if="carregando">Carregando...</p>
    
    <h2>Resultados ({{ resultados.length }})</h2>
    
    <div v-for="op in resultados" :key="op.Registro_ANS || op.CNPJ">
      <h3>{{ op.Nome_Fantasia ?? op.Razao_Social ?? "Nome não disponível" }}</h3>
      <p><strong>Representante:</strong> {{ op.Representante ?? "Não informado" }}</p>
      <p><strong>Cargo do Representante:</strong> {{ op.Cargo_Representante ?? "Não informado" }}</p>
      <p><strong>Região de Comercialização:</strong> {{ op.Regiao_de_Comercializacao ?? "Não informado" }}</p>
      <p><strong>Data de Registro ANS:</strong> {{ op.Data_Registro_ANS ?? "Não informado" }}</p>
      <p><strong>CNPJ:</strong> {{ op.CNPJ ?? "Não informado" }}</p>
      <p><strong>Registro ANS:</strong> {{ op.Registro_ANS ?? "Não informado" }}</p>
    </div>
  </div>
</template>

