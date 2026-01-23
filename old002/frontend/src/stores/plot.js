import { defineStore } from 'pinia'
import { ref, reactive, computed } from 'vue'
import { generatePlot, testPythonPlot, testRPlot } from '@/api/plot'
import { PLOT_TYPES, PLOT_TYPE_NAMES, LANGUAGE_TYPE } from '@/utils/constants'

export const usePlotStore = defineStore('plot', () => {
  // 状态定义
  const currentLanguage = ref(LANGUAGE_TYPE.PYTHON)
  const currentPlotType = ref('scatter')
  const loading = ref(false)
  const testingPython = ref(false)
  const testingR = ref(false)
  const plotResult = ref(null)
  const plotHistory = ref([])
  
  // 常量数据
  const plotTypes = reactive(PLOT_TYPES)
  const plotTypeNames = PLOT_TYPE_NAMES

  // Getter 计算属性
  const isPythonSelected = computed(() => currentLanguage.value === LANGUAGE_TYPE.PYTHON)
  const isRSelected = computed(() => currentLanguage.value === LANGUAGE_TYPE.R)
  const hasPlotResult = computed(() => plotResult.value && plotResult.value.success)
  const lastPlotTime = computed(() => {
    if (plotResult.value && plotResult.value.timestamp) {
      return new Date(plotResult.value.timestamp).toLocaleString()
    }
    return null
  })
  
  const plotHistoryCount = computed(() => plotHistory.value.length)

  // Action 方法
  const selectLanguage = (language) => {
    if (Object.values(LANGUAGE_TYPE).includes(language)) {
      currentLanguage.value = language
      plotResult.value = null
    } else {
      console.warn(`Invalid language: ${language}`)
    }
  }

  const selectPlotType = (type) => {
    if (Object.keys(plotTypeNames).includes(type)) {
      currentPlotType.value = type
    } else {
      console.warn(`Invalid plot type: ${type}`)
    }
  }

  const generatePlotAsync = async (options = {}) => {
    if (!currentLanguage.value) {
      throw new Error('请先选择编程语言')
    }
    
    loading.value = true
    plotResult.value = null
    
    try {
      const params = {
        language: currentLanguage.value,
        plot_type: currentPlotType.value,
        ...options
      }
      
      const result = await generatePlot(params)
      
      // 添加时间戳
      result.timestamp = new Date().toISOString()
      
      plotResult.value = result
      
      // 添加到历史记录(最多保存10条)
      if (result.success) {
        plotHistory.value.unshift({
          id: Date.now(),
          ...result,
          timestamp: result.timestamp
        })
        
        if (plotHistory.value.length > 10) {
          plotHistory.value.pop()
        }
      }
      
      return result
    } finally {
      loading.value = false
    }
  }

  const runTestAsync = async (language) => {
    if (![LANGUAGE_TYPE.PYTHON, LANGUAGE_TYPE.R].includes(language)) {
      throw new Error(`不支持的语言: ${language}`)
    }
    
    const isPython = language === LANGUAGE_TYPE.PYTHON
    
    if (isPython) {
      testingPython.value = true
    } else {
      testingR.value = true
    }
    
    plotResult.value = null
    
    try {
      const endpoint = isPython ? testPythonPlot : testRPlot
      const result = await endpoint()
      
      // 添加时间戳
      result.timestamp = new Date().toISOString()
      
      plotResult.value = result
      currentLanguage.value = language
      
      // 添加到历史记录
      if (result.success) {
        plotHistory.value.unshift({
          id: Date.now(),
          ...result,
          timestamp: result.timestamp
        })
        
        if (plotHistory.value.length > 10) {
          plotHistory.value.pop()
        }
      }
      
      return result
    } finally {
      if (isPython) {
        testingPython.value = false
      } else {
        testingR.value = false
      }
    }
  }

  const getPlotHistory = () => {
    return [...plotHistory.value]
  }

  const clearHistory = () => {
    plotHistory.value = []
  }

  const restoreFromHistory = (id) => {
    const item = plotHistory.value.find(item => item.id === id)
    if (item) {
      plotResult.value = item
      currentLanguage.value = item.language
      currentPlotType.value = item.plot_type
    }
  }

  const reset = () => {
    currentLanguage.value = LANGUAGE_TYPE.PYTHON
    currentPlotType.value = 'scatter'
    plotResult.value = null
    loading.value = false
    testingPython.value = false
    testingR.value = false
  }

  const exportState = () => {
    return {
      currentLanguage: currentLanguage.value,
      currentPlotType: currentPlotType.value,
      plotResult: plotResult.value,
      plotHistory: plotHistory.value
    }
  }

  const importState = (state) => {
    if (state.currentLanguage) currentLanguage.value = state.currentLanguage
    if (state.currentPlotType) currentPlotType.value = state.currentPlotType
    if (state.plotResult) plotResult.value = state.plotResult
    if (state.plotHistory) plotHistory.value = state.plotHistory
  }

  return {
    // 状态
    currentLanguage,
    currentPlotType,
    loading,
    testingPython,
    testingR,
    plotResult,
    plotHistory,
    plotTypes,
    plotTypeNames,
    
    // Getters
    isPythonSelected,
    isRSelected,
    hasPlotResult,
    lastPlotTime,
    plotHistoryCount,
    
    // Actions
    selectLanguage,
    selectPlotType,
    generatePlotAsync,
    runTestAsync,
    getPlotHistory,
    clearHistory,
    restoreFromHistory,
    reset,
    exportState,
    importState
  }
})