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

    resultados.value = await response.json();
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
    <input v-model="nomeOperadora" placeholder="Digite o nome da operadora..." />
    <button @click="buscarOperadoras">Buscar</button>
    
    <p v-if="carregando">Carregando...</p>
    
    <h2>Resultados ({{ resultados.length }})</h2>
    
    <div v-for="op in resultados" :key="op['Registro ANS']">
      <h3>{{ op.Nome_Fantasia || op.Razao_Social }}</h3>
      <p><strong>CNPJ:</strong> {{ op.CNPJ }}</p>
      <p><strong>Registro ANS:</strong> {{ op['Registro ANS'] }}</p>
    </div>
  </div>
</template>
