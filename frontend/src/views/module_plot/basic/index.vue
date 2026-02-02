<!-- 基础绘图列表页 -->
<template>
  <div class="plot-container">
    <!-- 按小类分卡片展示） -->
    <div class="card-container">
      <!-- 遍历小类分组（给 subcategory 兜底，避免 undefined） -->
      <div class="category-group" v-for="(group, subcategory) in groupedData" :key="subcategory">
        <h2 class="subcategory-title">{{ subcategory }}</h2>
        <!-- 使用 grid 布局替代 el-row 和 el-col，实现更紧凑的布局 -->
        <div class="card-grid">
          <router-link 
            v-for="item in group" 
            :key="item.code" 
            class="plot-card" 
            :to="getModulePath(item.code ?? '')"
          >
            <div class="card-inner">
              <!-- 图片区域：正方形 80x80px -->
              <div class="card-img-wrapper">
                <el-image :src="item.image ?? ''" fit="cover" lazy class="plot-image">
                  <template #error>
                    <div class="image-error">无图</div>
                  </template>
                </el-image>
              </div>
              <!-- 标题区域：高度 20px，单行居中 -->
              <div class="card-title">{{ item.name ?? '未命名' }}</div>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <!-- 分页组件 - 居中显示 -->
    <div class="pagination-container" v-if="pagination.total > 0">
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[12, 24, 36, 48]" 
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        background
      />
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "BasicPlot",
  inheritAttrs: false,
});

import { ref, reactive, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import PlotCategoryAPI, {
  PlotCategoryPageQuery,
  PlotCategoryTable,
} from "@/api/module_plot/category";

// 1. 初始化路由实例
const router = useRouter();

// 响应式数据
const loading = ref(false);
const rawData = ref<PlotCategoryTable[]>([]); // 当前页数据
const basicPlotCategoryName = ref("基础绘图");

// 新增：分页相关响应式数据
const pagination = reactive({
  currentPage: 1,    // 当前页码
  pageSize: 12,      // 每页默认显示数量
  total: 0           // 数据总条数
});

// 分页查询参数（关联分页组件数据）
const baseQueryFormData = reactive<PlotCategoryPageQuery>({
  page_no: pagination.currentPage,
  page_size: pagination.pageSize,
  category: basicPlotCategoryName.value,
  name: undefined,
  code: undefined,
  subcategory: undefined,
  created_time: undefined,
  updated_time: undefined,
  created_id: undefined,
  updated_id: undefined,
});

// 计算属性：按「小类（subcategory）」分组数据
const groupedData = computed(() => {
  return rawData.value.reduce((acc, item) => {
    const subcategory = (item.subcategory ?? '未分类') as string;
    if (!acc[subcategory]) {
      acc[subcategory] = [];
    }
    acc[subcategory].push(item);
    return acc;
  }, {} as Record<string, PlotCategoryTable[]>);
});

// 拼接跳转路径
const getModulePath = (code: string) => {
  if (!code) return '/404'
  const category = 'basic';
  return `/plot/${category}/${code}`
}

// 点击卡片跳转详情页方法
async function handleGoModule(code: string) {
  if (!code) {
    ElMessage.error("无效模块");
    return;
  }
  try {
    const category = 'basic';
    await router.push({
      path: `/plot/${category}/${code}`
    });
  } catch (error: any) {
    console.error("跳转模块页失败：", error);
    ElMessage.error("跳转模块页失败，请稍后重试");
  }
}

// 新增：处理每页数量变化
const handleSizeChange = (newPageSize: number) => {
  pagination.pageSize = newPageSize;
  pagination.currentPage = 1; // 每页数量变化时，重置为第1页
  loadBasicPlotData(); // 重新加载当前页数据
};

// 新增：处理当前页码变化
const handleCurrentChange = (newCurrentPage: number) => {
  pagination.currentPage = newCurrentPage;
  loadBasicPlotData(); // 重新加载当前页数据
};

// 加载基础绘图数据（适配分页组件，按需加载当前页数据）
async function loadBasicPlotData() {
  loading.value = true;
  rawData.value = []; // 清空原有当前页数据

  // 更新查询参数中的页码和每页数量
  baseQueryFormData.page_no = pagination.currentPage;
  baseQueryFormData.page_size = pagination.pageSize;

  try {
    const response = await PlotCategoryAPI.listPlotCategory(baseQueryFormData);
    const currentPageData = response.data.data.items || [];
    pagination.total = response.data.data.total || 0; // 更新总条数

    // 赋值当前页数据
    rawData.value.push(...currentPageData);
  } catch (error: any) {
    console.error("加载基础绘图数据失败：", error);
    ElMessage.error("加载数据失败，请稍后重试");
  } finally {
    loading.value = false;
  }
}

// 挂载时加载数据
onMounted(async () => {
  await loadBasicPlotData();
});
</script>

<style lang="scss" scoped>
.plot-container {
  padding: 20px;
  min-height: calc(100vh - 120px);
  box-sizing: border-box;
}

.card-container {
  margin-bottom: 30px;
}

.category-group {
  margin-bottom: 30px;
}

.subcategory-title {
  margin-bottom: 15px;
  padding-left: 10px;
  border-left: 4px solid #409eff;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

/* 使用 grid 布局实现紧凑卡片排列 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 90px); /* 容器宽度设为90px，为间距留出空间 */
  gap: 10px 15px; /* 行间距10px，列间距15px */
  justify-content: start; /* 左对齐 */
  padding: 5px 0;
}

.plot-card {
  display: block;
  width: 90px; /* 每个卡片容器宽度90px */
  text-decoration: none;
  color: inherit;
  outline: none;
}

.card-inner {
  width: 80px; /* 卡片内容宽度80px */
  height: 100px; /* 卡片内容高度100px */
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border-radius: 8px; /* 圆弧效果 */
  box-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid #e4e7ed;
  overflow: hidden; /* 防止内容溢出圆角 */
  position: relative;
  left: 5px; /* 微调位置，使卡片在90px容器中居中 */
}

.card-inner:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.15);
  border-color: #409eff;
}

.card-inner:hover .card-title {
  color: #409eff;
  background-color: #f0f7ff; /* 标题区域悬停背景色 */
}

.card-inner:hover .plot-image {
  filter: brightness(0.9) sepia(0.3) hue-rotate(180deg); /* 图片悬停变色效果 */
}

.card-img-wrapper {
  width: 80px;
  height: 80px; /* 正方形图片区域 */
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #f8f9fa; /* 图片区域背景色 */
  transition: all 0.2s ease;
  border-bottom: 1px solid #f0f0f0;
}

.plot-image {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover; /* 图片充满整个区域，保持比例裁剪 */
  transition: all 0.2s ease;
}

.image-error {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: #aaa;
  background-color: #f5f7fa;
}

.card-title {
  width: 80px;
  height: 20px; /* 标题区域高度 */
  text-align: center;
  font-size: 11px;
  font-weight: 500;
  color: #606266;
  line-height: 20px; /* 垂直居中 */
  transition: all 0.2s ease;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap; /* 单行显示 */
  padding: 0 4px; /* 左右留点空间 */
  background-color: #fff;
}

/* 分页样式 */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 0;
  margin-top: 10px;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .card-grid {
    grid-template-columns: repeat(auto-fill, 85px);
    gap: 8px 12px;
  }
  
  .plot-card {
    width: 85px;
  }
  
  .card-inner {
    width: 75px;
    height: 95px;
    left: 5px;
  }
  
  .card-img-wrapper {
    width: 75px;
    height: 75px;
  }
  
  .plot-image {
    width: 75px !important;
    height: 75px !important;
  }
  
  .card-title {
    width: 75px;
    height: 20px;
    font-size: 10px;
  }
  
  .image-error {
    width: 75px;
    height: 75px;
    font-size: 10px;
  }
}

@media (max-width: 768px) {
  .plot-container {
    padding: 15px;
  }
  
  .card-container {
    margin-bottom: 25px;
  }
  
  .category-group {
    margin-bottom: 25px;
  }
  
  .subcategory-title {
    font-size: 16px;
    margin-bottom: 12px;
  }
  
  .card-grid {
    grid-template-columns: repeat(auto-fill, 80px);
    gap: 6px 10px;
  }
  
  .plot-card {
    width: 80px;
  }
  
  .card-inner {
    width: 70px;
    height: 90px;
    left: 5px;
    border-radius: 6px;
  }
  
  .card-img-wrapper {
    width: 70px;
    height: 70px;
  }
  
  .plot-image {
    width: 70px !important;
    height: 70px !important;
  }
  
  .card-title {
    width: 70px;
    height: 20px;
    font-size: 10px;
  }
  
  .image-error {
    width: 70px;
    height: 70px;
    font-size: 9px;
  }
}

@media (max-width: 480px) {
  .plot-container {
    padding: 12px 10px;
  }
  
  .card-grid {
    grid-template-columns: repeat(auto-fill, 75px);
    gap: 5px 8px;
    justify-content: space-around; /* 小屏幕时平均分布 */
  }
  
  .plot-card {
    width: 75px;
  }
  
  .card-inner {
    width: 65px;
    height: 85px;
    left: 5px;
    border-radius: 5px;
  }
  
  .card-img-wrapper {
    width: 65px;
    height: 65px;
  }
  
  .plot-image {
    width: 65px !important;
    height: 65px !important;
  }
  
  .card-title {
    width: 65px;
    height: 20px;
    font-size: 9px;
  }
  
  .image-error {
    width: 65px;
    height: 65px;
    font-size: 8px;
  }
}
</style>