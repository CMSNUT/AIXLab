<!-- 功能 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <transition name="search-fade">
    <div v-show="visible && !isSearchGlobalCollapsed" class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        label-suffix=":"
        :inline="true"
        @submit.prevent="handleQuery"
      >
        <el-form-item label="功能名称" prop="name">
          <el-input v-model="queryFormData.name" placeholder="请输入功能名称" clearable />
        </el-form-item>
        <el-form-item label="研究领域" prop="field">
          <el-input v-model="queryFormData.field" placeholder="请输入研究领域" clearable />
        </el-form-item>
        <el-form-item label="功能类别" prop="category">
          <el-input v-model="queryFormData.category" placeholder="请输入功能类别" clearable />
        </el-form-item>
        <el-form-item label="备注/描述" prop="description">
          <el-input v-model="queryFormData.description" placeholder="请输入备注/描述" clearable />
        </el-form-item>
        
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item>
          <el-button
            v-hasPerm="['module_lab:calc:query']"
            type="primary"
            icon="search"
            @click="handleQuery"
          >
            查询
          </el-button>
          <!-- 展开/收起 -->
          <template v-if="isExpandable">
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
              {{ isExpand ? "收起" : "展开" }}
              <el-icon>
                <template v-if="isExpand">
                  <ArrowUp />
                </template>
                <template v-else>
                  <ArrowDown />
                </template>
              </el-icon>
            </el-link>
          </template>
        </el-form-item>
      </el-form>
    </div>
    </transition>

    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <!-- 左侧：测试列表 + 提示 tooltip -->
          <span class="card-header__title">
            功能列表
            <el-tooltip content="功能列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
          </span>
        </div>
      </template>

      <!-- 表格区域：系统配置列表 -->
      <el-table
        ref="tableRef"
        v-loading="loading"
        :data="pageTableData"
        highlight-current-row
        class="data-table__content"
        :height="450"
        border
        stripe
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'selection')?.show"
          type="selection"
          min-width="55"
          align="center"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'index')?.show"
          fixed
          label="序号"
          min-width="60"
        >
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'name')?.show"
          label="功能名称"
          prop="name"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'field')?.show"
          label="研究领域"
          prop="field"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'category')?.show"
          label="功能类别"
          prop="category"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'description')?.show"
          label="备注/描述"
          prop="description"
          min-width="140"
        />

        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'image')?.show"
          label="图片"
          prop="image"
          min-width="70"
        >
          <template #default="scope">                               
            <el-image
              v-if="scope.row.image" 
              :src="scope.row.image"  
              style="width: 50px; height: 50px;"  
              fit="cover"
              lazy
              :preview-src-list="[scope.row.image]"
              :preview-teleported="true"
            />
          </template>
        </el-table-column>
        
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
          fixed="right"
          label="操作"
          align="center"
          min-width="180"
        >
          <template #default="scope">
            <el-button
              v-hasPerm="['module_lab:calc:detail']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDetail(scope.row)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="total"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          @pagination="loadingData"
        />
      </template>
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "LabCalcList",
  inheritAttrs: false,
});

import { ref, reactive, onMounted } from "vue";
import { QuestionFilled, ArrowUp, ArrowDown} from "@element-plus/icons-vue";
import { useDictStore } from "@/store";
import { useRouter, useRoute } from 'vue-router'

import LabCalcAPI, {
  LabCalcPageQuery,
  LabCalcTable,
} from "@/api/module_lab/calc";

const visible = ref(true);
const isExpand = ref(false);
const isExpandable = ref(true);
const queryFormRef = ref();
const total = ref(0);
const loading = ref(false);
const isSearchGlobalCollapsed = ref(true);

// 字典仓库与需要加载的字典类型
const dictStore = useDictStore();
const dictTypes: any = [
];

// 分页表单
const pageTableData = ref<LabCalcTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "name", label: "功能名称", show: true },
  { prop: "field", label: "研究领域", show: true },
  { prop: "category", label: "功能类别", show: true },
  { prop: "description", label: "备注/描述", show: true },
  { prop: "image", label: "图片", show: true },
  { prop: "operation", label: "操作", show: true },
]);

// 分页查询参数
const queryFormData = reactive<LabCalcPageQuery>({
  page_no: 1,
  page_size: 10,
  name: undefined,
  field: undefined,
  category: undefined,
  description: undefined,
  created_time: undefined,
  updated_time: undefined,
  created_id: undefined,
  updated_id: undefined,
});


// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await LabCalcAPI.listLabCalc(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

const router = useRouter()
const route = useRoute()



const handleOpenDetail = (row: any) => {
//   router.push({
//     path: '/lab/calc/detail',
//     query: {
//       id: row.id
//     }
//   })
    const routeData = router.resolve({
        path: '/lab/calc/detail',
        query: { id: row.id }
    })
    // 构建完整URL
    const url = window.location.origin + routeData.href

    // 打开新窗口
    window.open(url, '_blank')
}



const getFileName = (fullPath: string): string => {
  if (!fullPath || typeof fullPath !== 'string') return '未知文件';
  
  // 匹配最后一个 "/" 后面的内容（兼容 http 路径和本地路径）
  const fileName = fullPath.split('/').pop() || '未知文件';
  
  // 若路径包含 "\"（Windows 路径，可选兼容）
  return fileName.split('\\').pop() || fileName;
};

onMounted(async () => {
  // 预加载字典数据
  if (dictTypes.length > 0) {
    await dictStore.getDict(dictTypes);
  }
  loadingData();
});
</script>

<style lang="scss" scoped></style>
