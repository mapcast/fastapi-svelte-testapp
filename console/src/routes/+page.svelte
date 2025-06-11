<script>
  import { onMount } from 'svelte';
  let products = [];
  let promotions = [];
  let categories = [];
  let loading = {
    products: true,
    promotions: true,
    categories: true
  };
  let error = {
    products: '',
    promotions: '',
    categories: ''
  };

  onMount(async () => {
    // 상품 목록 가져오기
    try {
      const res = await fetch('http://localhost:8000/products/?sort_by=created_at&order=desc&limit=8');
      if (!res.ok) throw new Error('상품 정보를 불러오지 못했습니다');
      products = await res.json();
    } catch (e) {
      error.products = e.message;
    } finally {
      loading.products = false;
    }

    // 프로모션 정보 가져오기
    try {
      const res = await fetch('http://localhost:8000/promotions/');
      if (!res.ok) throw new Error('프로모션 정보를 불러오지 못했습니다');
      promotions = await res.json();
    } catch (e) {
      error.promotions = e.message;
    } finally {
      loading.promotions = false;
    }

    // 카테고리 정보 가져오기
    try {
      const res = await fetch('http://localhost:8000/categories/');
      if (!res.ok) throw new Error('카테고리 정보를 불러오지 못했습니다');
      categories = await res.json();
    } catch (e) {
      error.categories = e.message;
    } finally {
      loading.categories = false;
    }
  });
</script>

<main>
  <!-- 프로모션 배너 섹션 -->
  <section class="promotions">
    <h2>진행중인 프로모션</h2>
    {#if loading.promotions}
      <p>로딩 중...</p>
    {:else if error.promotions}
      <p class="error">{error.promotions}</p>
    {:else if promotions.length === 0}
      <p>진행중인 프로모션이 없습니다.</p>
    {:else}
      <div class="promotion-grid">
        {#each promotions as promotion}
          <div class="promotion-card">
            <img src={promotion.image_url} alt={promotion.title} />
            <h3>{promotion.title}</h3>
            <p>{promotion.description}</p>
          </div>
        {/each}
      </div>
    {/if}
  </section>

  <!-- 카테고리 메뉴 섹션 -->
  <section class="categories">
    <h2>카테고리</h2>
    {#if loading.categories}
      <p>로딩 중...</p>
    {:else if error.categories}
      <p class="error">{error.categories}</p>
    {:else if categories.length === 0}
      <p>등록된 카테고리가 없습니다.</p>
    {:else}
      <div class="category-grid">
        {#each categories as category}
          <a href="/category/{category.id}" class="category-card">
            <h3>{category.name}</h3>
            {#if category.description}
              <p>{category.description}</p>
            {/if}
          </a>
        {/each}
      </div>
    {/if}
  </section>

  <!-- 최신 상품 섹션 -->
  <section class="products">
    <h2>최신 상품</h2>
    {#if loading.products}
      <p>로딩 중...</p>
    {:else if error.products}
      <p class="error">{error.products}</p>
    {:else if products.length === 0}
      <p>등록된 상품이 없습니다.</p>
    {:else}
      <div class="product-grid">
        {#each products as product}
          <div class="product-card">
            {#if product.images && product.images.length > 0}
              <img src={product.images[0].image_url} alt={product.name} />
            {:else}
              <div class="no-image">이미지 없음</div>
            {/if}
            <h3>{product.name}</h3>
            <p class="price">{product.price.toLocaleString()}원</p>
            <p class="description">{product.description}</p>
            <div class="stock">재고: {product.stock}개</div>
          </div>
        {/each}
      </div>
    {/if}
  </section>
</main>

<style>
  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  section {
    margin-bottom: 40px;
  }

  h2 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
  }

  .error {
    color: red;
  }

  /* 프로모션 스타일 */
  .promotion-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }

  .promotion-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s;
  }

  .promotion-card:hover {
    transform: translateY(-5px);
  }

  .promotion-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }

  .promotion-card h3 {
    padding: 15px;
    margin: 0;
    font-size: 18px;
  }

  .promotion-card p {
    padding: 0 15px 15px;
    margin: 0;
    color: #666;
  }

  /* 카테고리 스타일 */
  .category-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
  }

  .category-card {
    text-decoration: none;
    color: inherit;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    transition: background-color 0.2s;
  }

  .category-card:hover {
    background-color: #f5f5f5;
  }

  /* 상품 스타일 */
  .product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }

  .product-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s;
  }

  .product-card:hover {
    transform: translateY(-5px);
  }

  .product-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }

  .no-image {
    width: 100%;
    height: 200px;
    background-color: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
  }

  .product-card h3 {
    padding: 15px 15px 5px;
    margin: 0;
    font-size: 18px;
  }

  .product-card .price {
    padding: 0 15px;
    margin: 0;
    font-weight: bold;
    color: #e44d26;
  }

  .product-card .description {
    padding: 5px 15px;
    margin: 0;
    color: #666;
    font-size: 14px;
  }

  .product-card .stock {
    padding: 5px 15px 15px;
    margin: 0;
    color: #666;
    font-size: 14px;
  }
</style>
