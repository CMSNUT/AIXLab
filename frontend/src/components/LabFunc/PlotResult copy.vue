<template>
    <el-card class="plot-card" shadow="hover">
        <div class="add-calc-container">
            <h3 class="calc-title">加法计算</h3>
            <div class="input-group">
                <el-input-number v-model="numA" placeholder="请输入第一个数" class="num-input" :min="-999999" :max="999999"
                    step="1" clearable />
                <span class="calc-symbol">+</span>
                <el-input-number v-model="numB" placeholder="请输入第二个数" class="num-input" :min="-999999" :max="999999"
                    step="1" clearable />
            </div>
            <el-button type="primary" class="calc-btn" @click="handleAddCalc" :loading="loading"
                icon="el-icon-calculator">
                立即计算
            </el-button>
            <div class="result-area" v-if="calculationResult !== null || error">
                <el-tag type="success" v-if="calculationResult !== null && !error" class="result-tag">
                    计算结果：{{ numA }} + {{ numB }} = {{ calculationResult }}
                </el-tag>
                <el-tag type="danger" v-if="error" class="error-tag">
                    计算失败：{{ error }}
                </el-tag>
            </div>
        </div>
    </el-card>
</template>

<script setup lang="ts">
import LabPlotAPI from "@/api/module_lab/plot";
import { ref } from 'vue'

// 响应式数据
const numA = ref(null) // 第一个加数
const numB = ref(null) // 第二个加数
const calculationResult = ref(null) // 计算结果
const loading = ref(false) // 按钮loading防重
const error = ref('') // 错误信息

// 加法计算核心逻辑
async function handleAddCalc() {
    // 重置状态
    calculationResult.value = null
    error.value = ''

    // 前置校验：数字合法性验证
    const a = parseFloat(numA.value)
    const b = parseFloat(numB.value)

    // 1. 前端本地校验，减少无效请求
    if (isNaN(a) || isNaN(b)) {
        error.value = '请输入有效的数字'
        return
    }

    try {
        // 2. 开启loading，防止重复点击
        loading.value = true

        // 3. 调用API
        const response = await LabPlotAPI.add({ a, b })

        console.log(response)

        // 4. 处理成功响应（匹配后端统一响应格式）
        if (response.data.success) {
            // 提取R服务返回的计算结果
            calculationResult.value = response.data.data.data.result
        } else {
            // 处理R服务返回的业务错误
            error.value = response.data.error || '计算失败，请重试'
        }
    } catch (err) {
        // 5. 处理网络/后端异常
        error.value = err.message || '服务器连接失败，请稍后重试'
        console.error('加法计算异常:', err)
    } finally {
        // 6. 无论成功失败，关闭loading
        loading.value = false
    }
}
</script>