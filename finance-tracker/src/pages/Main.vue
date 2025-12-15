<template>
    <div class="main-page">
        <MainHeader />
        <MainBalance />
        <!-- <MainQuickInput /> -->
        <MainChart />
        <MainGrid />
        <MainTransactions />
    </div>
</template>

<script setup lang="ts">
import MainChart from '@/components/Main/MainChart.vue';
import MainHeader from '@/components/Main/MainHeader.vue';
import MainBalance from '@/components/Main/MainBalance.vue';
// import MainQuickInput from '@/components/Main/MainQuickInput.vue';
import MainTransactions from '@/components/Main/MainTransactions.vue';
import MainGrid from '@/components/Main/MainGrid.vue';
</script>

<style scoped lang="scss">
.main-page {
    max-width: 66rem;
    width: 100%;
    margin: 0 auto;
    padding: 2rem;
    height: 100dvh;
}
</style>