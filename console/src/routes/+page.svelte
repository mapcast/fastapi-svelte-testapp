<script>
  import { onMount } from 'svelte';
  let products = [];
  let loading = true;
  let error = '';

  onMount(async () => {
    try {
      const res = await fetch('http://localhost:8000/products/');
      if (!res.ok) throw new Error('상품 정보를 불러오지 못했습니다');
      products = await res.json();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  });
</script>

<h1>상품 목록</h1>

{#if loading}
  <p>로딩 중...</p>
{:else if error}
  <p style="color:red">{error}</p>
{:else if products.length === 0}
  <p>등록된 상품이 없습니다.</p>
{:else}
  <ul>
    {#each products as product}
      <li>
        <strong>{product.name}</strong> - {product.price}원 (재고: {product.stock})<br />
        <small>{product.description}</small>
      </li>
    {/each}
  </ul>
{/if}
