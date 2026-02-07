<template>
    <!-- 数据读取 -->
    <el-card class="plot-card">
        <template #header>
            <div class="plot-card-header">
                <span>绘图数据</span>
                <div class="plot-card-header-right">
                    <el-button type="text">
                        <el-icon class="plot-card-header-reset-icon">
                            <Refresh />
                        </el-icon>
                        <span class="plot-card-header-title">重置数据</span>
                    </el-button>
                </div>
            </div>
        </template>

        <div class="plot-data-box">
            <div class="plot-data-params-box">
                <div class="plot-data-params-box-title">
                    <div class="upload-plot-header">
                        <span>上传数据</span>
                        <el-tooltip content="数据提示，从方法-数据的数据表中获取" placement="top">
                            <el-icon>
                                <InfoFilled />
                            </el-icon>
                        </el-tooltip>
                    </div>

                    <el-upload ref="upload" class="upload-demo" action="" :limit="1" :on-exceed="handleExceed"
                        :auto-upload="false">
                        <template #trigger>
                            <el-button type="primary">选择数据文件</el-button>
                        </template>
                        <el-button class="ml-3" type="success" @click="submitUpload">
                            确认上传数据
                        </el-button>
                        <template #tip>
                            <div class="el-upload__tip text-red">
                                limit 1 file, new file will cover the old file
                            </div>
                        </template>
                    </el-upload>

                    <el-button type="warning">下载示例数据</el-button>

                    <el-button type="success">
                        <el-icon size="16" color="white">
                            <circle-check-filled />
                        </el-icon> 验证成功
                    </el-button>
                </div>

            </div>

        </div>
    </el-card>
    <!-- 数据结束-->
</template>

<script lang="ts" setup>

</script>

<style scoped lang="scss">
/* 上传区域样式 */
.plot-data-box {
    width: 100%;
    padding: 0 30px 30px 25px;
    box-sizing: border-box;
    background: #fff;
}

.plot-data-params-box {
    width: 100%;
    padding-top: 40px;
}

.upload-plot-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    font-weight: 500;
}

.file-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    padding: 8px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.filename {
    font-weight: 500;
    color: #409eff;
}

.upload-tips {
    font-size: 12px;
    color: #909399;
    margin-bottom: 16px;
}

.verify-status {
    text-align: center;
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
</style>