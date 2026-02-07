<template>
  <div class="plot-container">
    <!-- 页面头部 -->
    <div class="plot-header-box">
      <div class="plot-header-content">
        <div class="plot-header-title">
          {{ plotStore.currentPlot?.field }} - {{ plotStore.currentPlot?.category }} - {{ plotStore.currentPlot?.name }}
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="plot-main-content">
      <!-- 左侧绘图区域 -->
      <div class="plot-left-section">
        <!-- 使用 store hook 获取数据 -->
        <PlotDataUpload />

        <PlotParamSet />

        <PlotResult />

        <!-- 结果展示 -->
        <el-card class="plot-card">

        </el-card>
        <!-- 结果结束 -->

      </div>
      <!-- 左侧区域结束 -->

      <!-- 右侧文献区域 -->
      <div class="plot-right-section">
        <el-card>
          我是很多文献
        </el-card>
      </div>
      <!-- 右侧区域结束 -->

    </div>

  </div>
</template>

<script setup lang="ts">
defineOptions({
    name: "LabPlotDetail",
    inheritAttrs: false,
});

import { onMounted, watch } from "vue";
import { useRoute, onBeforeRouteUpdate } from "vue-router";
import { usePlotStoreHook } from "@/store";

const plotStore = usePlotStoreHook()
const route = useRoute()

// 从路由获取ID并加载数据
const loadPlotData = (id: number) => {
  if (id) {
    plotStore.fetchPlotDetail(Number(id));
  }
}

onMounted(() => {
  if (route.query.id) {
    loadPlotData(Number(route.query.id));
  }
})

// 路由更新前触发
onBeforeRouteUpdate((to, from, next) => {
  const newId = Number(to.query.id);
  const oldId = Number(from.query.id);

  if (newId && newId !== oldId) {
    loadPlotData(newId);
  }
  next();
})

// 监听路由参数变化
watch(
  () => route.query.id,
  (newId, oldId) => {
    if (newId && newId !== oldId) {
      loadPlotData(Number(newId));
    }
  },
  { immediate: false }
)


</script>

<style scoped>
.plot-container {
  min-width: 1200px;
  background-color: #f5f7fa;
  min-height: 100vh;
  margin: 0 auto;
}

/* 头部样式 */
.plot-header-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
  width: 100%;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.plot-header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.plot-header-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  box-sizing: border-box;
  font-size: 20px;
  font-weight: 700;
}

/* 主要内容布局 */
.plot-main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0;
  display: grid;
  grid-template-columns: 70% 1fr;
  gap: 10px;
}

/* 左侧区域确保无内边距 */
.plot-left-section {
  padding: 0;
  width: 100%;
  border-radius: 0;
}

.plot-right-section {
  padding: 0;
  width: 100%;
  border-radius: 0;
}

/* 参数卡片样式 */
:deep(.plot-card) {
  width: 100%;
  padding: 0 !important;
  margin: 10px 0 !important;
  margin-bottom: 25px !important;
  border-radius: 10px 10px 0 0;
  overflow: hidden;
}

/* 清除卡片默认头部内边距 */
:deep(.plot-card .el-card__header) {
  padding: 0;
  margin: 0;
}

/* 清除卡片默认主体内边距 */
:deep(.plot-card .el-card__body) {
  padding: 0;
}

/* 卡片头部样式 */
.plot-card-header {
  font-weight: 700;
  font-size: 14px;
  color: white;
  width: 100%;
  height: 35px;
  background: #F19F55;
  display: flex;
  align-items: center;
  padding: 0 15px;
  box-sizing: border-box;
  justify-content: space-between;
}

.plot-card-header-right {
  height: 100%;
  display: flex;
  align-items: center;
}

.plot-card-header-reset-icon {
  color: white;
  font-size: 18px;
  margin-right: 2px;
}

.plot-card-header-title {
  font-size: 12px;
  font-weight: 400;
  color: #fff;
}


.plot-header-actions {
  display: flex;
  gap: 10px;
}



/* 参数项样式 */
.param-item {
  margin-bottom: 16px;
}

.param-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
  font-weight: 500;
}

.param-label.tips-text {
  color: #909399;
}

.color-group {
  display: flex;
  gap: 12px;
}

/* 折叠面板样式 */
:deep(.el-collapse-item__plot-header) {
  font-weight: 600;
  color: #303133;
}

:deep(.el-collapse-item__content) {
  padding: 20px;
  background-color: #fafafa;
  border-radius: 0 0 4px 4px;
}

/* 提交按钮区域 */
.submit-section {
  text-align: center;
  margin: 20px 0;
}

.submit-section .el-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  background: linear-gradient(135deg, #f46e2f 0%, #ff8c00 100%);
  border: none;
}

.submit-section .el-button:hover {
  background: linear-gradient(135deg, #e55e1f 0%, #e67c00 100%);
}

/* 结果区域样式 */
.plot-left-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
}

.result-plot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
}

.result-tabs {
  display: flex;
  gap: 30px;
}

.result-tab {
  padding: 8px 0;
  cursor: pointer;
  color: #888;
  font-weight: 600;
  position: relative;
  transition: color 0.3s;
}

.result-tab:hover {
  color: #f46e2f;
}

.tab-active {
  color: #f46e2f;
}

.tab-active::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -1px;
  width: 100%;
  height: 2px;
  background: #f46e2f;
}

.result-actions {
  display: flex;
  gap: 10px;
}

/* 结果内容样式 */
.result-content {
  padding: 20px;
}

.result-block {
  margin-bottom: 30px;
}

.result-plot-title {
  position: relative;
  padding-left: 12px;
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.result-plot-title::after {
  content: "";
  position: absolute;
  left: 0;
  top: 2px;
  width: 5px;
  height: 20px;
  background: #f46e2f;
}

.result-intro {
  padding: 16px;
  background: #f7f7f7;
  border-radius: 4px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #555;
  line-height: 1.6;
}

.result-intro div {
  margin-bottom: 8px;
}

.result-intro strong {
  color: #303133;
}

.result-image {
  text-align: center;
  background: #f7f7f7;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.plot-image {
  max-width: 100%;
  height: 400px;
  object-fit: contain;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #909399;
}

.image-error .el-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

/* 表格样式 */
.result-table {
  margin: 16px 0;
  border-radius: 4px;
  overflow: hidden;
}

:deep(.result-table .el-table__plot-header) {
  background-color: #f5f7fa;
}

:deep(.result-table th) {
  background-color: #f5f7fa;
  color: #303133;
  font-weight: 600;
}

/* 解释说明样式 */
.result-explain {
  padding: 16px;
  background: #f7f7f7;
  border-radius: 4px;
  margin-top: 16px;
  font-size: 14px;
  color: #555;
}

/* 方法学内容样式 */
.methodology-content {
  padding: 16px;
  background: #f7f7f7;
  border-radius: 4px;
  font-size: 14px;
  color: #555;
  line-height: 1.6;
}

.methodology-content>div {
  margin-bottom: 16px;
}

.methodology-content p {
  margin: 8px 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .plot-main-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {

  .plot-header-content,
  .plot-main-content {
    padding: 0 12px;
  }

  .plot-header-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .action-buttons {
    width: 100%;
    justify-content: space-between;
  }

  .result-plot-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .result-tabs {
    width: 100%;
    justify-content: space-between;
    gap: 10px;
  }

  .result-actions {
    width: 100%;
    justify-content: center;
  }
}
</style>