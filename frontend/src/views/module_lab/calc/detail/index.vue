<template>
    <div class="app-container">
        <h1> {{ detailData?.name }}</h1>
    </div>
    
</template>

<script setup lang="ts">
    defineOptions({
    name: "LabCalcDetail",
    inheritAttrs: false,
    });

//    console.log("测试id", useRoute().query.id)

    import LabCalcAPI from "@/api/module_lab/calc";
    import { ref, onMounted } from 'vue' 
    import { useRoute, onBeforeRouteUpdate } from 'vue-router'

    const route = useRoute()
    const detailData = ref<any>({})

    const fetchDetail = async (id: number) => {
        try {
            // 加强 ID 合法性校验
            if (!id || isNaN(id) || id <= 0) {
                console.error("无效的 ID 参数：必须是大于 0 的数字")
                detailData.value = {} // 重置数据，避免残留旧数据
                return
            }

            const res = await LabCalcAPI.detailLabCalc(id)
            // 校验接口返回数据格式，避免异常数据赋值
            if (res && res.data && res.data.data) {
            detailData.value = res.data.data
            // console.log("数据获取成功：", detailData.value)
            } else {
            // console.warn("接口返回数据格式异常，重置为空数据")
            detailData.value = {}
            }
        } catch (error) {
            // console.error("获取详情失败：", error)
            detailData.value = {} // 异常时重置数据，避免页面展示旧数据
        }
    }
 
    onMounted(() => {
        if (route.query.id) {
            fetchDetail(Number(route.query.id))
        }
    })

    // 4. 修复：路由更新前触发（组件复用场景，优先用 to 中的新参数）
    onBeforeRouteUpdate((to, from, next) => {
    console.log('路由更新触发（守卫）：', to.query.id, '→ 旧：', from.query.id)
    const newId = Number(to.query.id)
    const oldId = Number(from.query.id)

    // 确保新老 ID 不同且有效，再请求
    if (newId && newId !== oldId) {
        fetchDetail(newId)
    }
    // 必须调用 next() 放行路由
    next()
    })

    // 5. 兜底方案：监听路由参数变化（确保 100% 捕获 id 变更）
    watch(
        () => route.query.id, // 监听路由中的 id 参数
        (newId, oldId) => {
            // console.log('路由参数监听触发：', newId, '→ 旧：', oldId)
            if (newId && newId !== oldId) {
            fetchDetail(Number(newId))
            }
        },
        { immediate: false, deep: false } // 非首次执行，无需深度监听
    )

</script>

<style lang="scss" scoped></style>