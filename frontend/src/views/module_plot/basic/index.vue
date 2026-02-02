<!-- 基础绘图列表页（点击卡片跳转详情页，保留id、解决TS错误） -->
<template>
  <div class="basic-plot-container">
    <!-- 核心内容：按小类分卡片展示（点击卡片跳转详情页） -->
    <div class="card-container">
      <!-- 遍历小类分组（给 subcategory 兜底，避免 undefined） -->
      <div class="category-group" v-for="(group, subcategory) in groupedData" :key="subcategory">
        <h2 class="subcategory-title">{{ subcategory }}</h2>
        <!-- 该小类下的所有卡片（绑定点击事件，传递id跳转） -->
        <div class="card-list">
          <div 
            class="plot-card" 
            v-for="item in group" 
            :key="item.code"
            @click="handleGoModule(item.code ?? '')"
          >
            <div class="card-img-wrapper">
              <el-image
                :src="item.image ?? ''"
                fit="cover"
                lazy
              >
                <!-- 图片加载失败占位 -->
                <template #error>
                  <div class="image-error">暂无图片</div>
                </template>
              </el-image>
            </div>
            <!-- 卡片标题（给 name 兜底，避免 undefined） -->
            <div class="card-title">{{ item.name ?? '未命名模块' }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "BasicPlot",
  inheritAttrs: false,
});

import { ref, reactive, onMounted, computed } from "vue";
import { useRouter } from "vue-router"; // 重新引入路由跳转依赖
import { ElMessage } from "element-plus";
import PlotCategoryAPI, {
  PlotCategoryPageQuery,
  PlotCategoryTable,
} from "@/api/module_plot/category";

// 1. 初始化路由实例（用于跳转详情页）
const router = useRouter();

// 响应式数据
const loading = ref(false);
const rawData = ref<PlotCategoryTable[]>([]); // 原始基础绘图数据
const basicPlotCategoryName = ref("基础绘图"); // 基础绘图大类名称（可根据实际接口值修改）

// 分页查询参数（page_size设为接口允许的最大值100，避免超限）
const baseQueryFormData = reactive<PlotCategoryPageQuery>({
  page_no: 1,
  page_size: 100, // 符合接口校验规则（≤100）
  category: basicPlotCategoryName.value, // 仅查询「基础绘图」大类
  name: undefined,
  code: undefined,
  subcategory: undefined,
  created_time: undefined,
  updated_time: undefined,
  created_id: undefined,
  updated_id: undefined,
});

// 计算属性：按「小类（subcategory）」分组数据（给 subcategory 兜底，避免 undefined）
const groupedData = computed(() => {
  return rawData.value.reduce((acc, item) => {
    // 空值兜底：undefined 转为 '未分类'，确保为 string 类型
    const subcategory = (item.subcategory ?? '未分类') as string;
    // 按小类分组
    if (!acc[subcategory]) {
      acc[subcategory] = [];
    }
    acc[subcategory].push(item);
    return acc;
  }, {} as Record<string, PlotCategoryTable[]>);
});

// 2. 新增：点击卡片跳转详情页方法（接收id参数）
async function handleGoModule(code: string) {
  if (!code) {
    ElMessage.error("无效模块");
    return;
  }
  try {
    // 方式1：使用 path 跳转（推荐，更明确）
    // await router.push({
    //   path: `/plot/${category}/${code}`
    // });
    
    // 或者方式2：使用 name 跳转（需要确保路由配置中的 name 匹配）
     await router.push({
      name: "PlotModule", // 使用路由名称
      params: { 
        category: 'basic', // 固定为 basic
        code: code         // 模块编码
      }
    });
  } catch (error: any) {
    console.error("跳转模块页失败：", error);
    ElMessage.error("跳转模块页失败，请稍后重试");
  }
}

// 加载基础绘图数据（循环分页请求，避免page_size超限）
async function loadBasicPlotData() {
  loading.value = true;
  rawData.value = []; // 清空原有数据
  let currentPage = 1;
  let totalCount = 0;

  try {
    // 循环分页请求，直到获取所有数据
    while (true) {
      // 构造当前页查询参数
      const currentQuery = {
        ...baseQueryFormData,
        page_no: currentPage,
      };

      const response = await PlotCategoryAPI.listPlotCategory(currentQuery);
      const currentPageData = response.data.data.items || [];
      totalCount = response.data.data.total || 0;

      // 合并当前页数据到原始数据中
      rawData.value.push(...currentPageData);

      // 终止条件：当前页数据为空，或已获取所有数据
      if (currentPageData.length === 0 || rawData.value.length >= totalCount) {
        break;
      }

      // 页码自增，请求下一页
      currentPage++;
    }
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
// 整体布局
.basic-plot-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
  box-sizing: border-box;
}

// 页面头部
.page-header {
  text-align: center;
  margin-bottom: 32px;

  .page-title {
    font-size: 28px;
    font-weight: 700;
    color: #333;
    margin: 0 0 8px 0;
  }

  .page-desc {
    font-size: 16px;
    color: #666;
    margin: 0;
  }
}

// 小类分组容器
.category-group {
  margin-bottom: 40px;

  .subcategory-title {
    font-size: 20px;
    font-weight: 600;
    color: #2f4f4f;
    margin: 0 0 16px 0;
    padding-left: 8px;
    border-left: 4px solid #4169e1;
  }
}

// 卡片列表（横向排列，自动换行）
.card-list {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  justify-content: flex-start;
}

// 绘图卡片（恢复点击跳转样式，提示用户可点击）
.plot-card {
  width: 180px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  // 恢复可点击光标，提示用户可点击跳转
  cursor: pointer;
  transition: all 0.3s ease; // 过渡效果包含阴影和位移

  &:hover {
    // 恢复hover上浮+加深阴影，强化可点击交互提示
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }

  // 卡片图片容器
  .card-img-wrapper {
    width: 100%;
    height: 180px;
    background-color: #f8f9fa;

    .el-image {
      width: 100%;
      height: 100%;
    }

    .image-error {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #999;
      font-size: 14px;
    }
  }

  // 卡片标题
  .card-title {
    padding: 12px 8px;
    text-align: center;
    font-size: 14px;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    background-color: #fff;
  }
}
</style>