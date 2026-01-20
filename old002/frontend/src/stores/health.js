import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { checkHealth } from "@/api/health";
import { formatServiceStatus } from "@/utils/helpers";

export const useHealthStore = defineStore("health", () => {
  // 状态
  const mainStatus = ref("检查中...");
  const pythonStatus = ref("检查中...");
  const rStatus = ref("检查中...");
  const loading = ref(false);
  const lastChecked = ref(null);
  const checkHistory = ref([]);
  const autoCheckTimer = ref(null);

  // Getters
  const allServicesHealthy = computed(() => {
    return (
      mainStatus.value === "正常" &&
      pythonStatus.value === "正常" &&
      rStatus.value === "正常"
    );
  });

  const hasUnhealthyServices = computed(() => {
    return (
      mainStatus.value === "异常" ||
      pythonStatus.value === "异常" ||
      rStatus.value === "未启动"
    );
  });

  const formattedLastChecked = computed(() => {
    if (!lastChecked.value) return "从未检查";
    return lastChecked.value.toLocaleString("zh-CN");
  });

  // Actions
  const checkServices = async () => {
    loading.value = true;

    try {
      const status = await checkHealth();

      const oldStatus = {
        main: mainStatus.value,
        python: pythonStatus.value,
        r: rStatus.value,
      };

      mainStatus.value = formatServiceStatus(status.main_service);
      pythonStatus.value = formatServiceStatus(status.python_service);
      rStatus.value = formatServiceStatus(status.r_service);

      lastChecked.value = new Date();

      // 记录检查历史
      checkHistory.value.unshift({
        timestamp: lastChecked.value.toISOString(),
        status: {
          main: mainStatus.value,
          python: pythonStatus.value,
          r: rStatus.value,
        },
        changed:
          mainStatus.value !== oldStatus.main ||
          pythonStatus.value !== oldStatus.python ||
          rStatus.value !== oldStatus.r,
      });

      // 最多保留50条记录
      if (checkHistory.value.length > 50) {
        checkHistory.value.pop();
      }

      return {
        main: mainStatus.value,
        python: pythonStatus.value,
        r: rStatus.value,
        timestamp: lastChecked.value,
      };
    } catch (error) {
      console.error("Health check failed:", error);

      const oldStatus = {
        main: mainStatus.value,
        python: pythonStatus.value,
        r: rStatus.value,
      };

      mainStatus.value = "异常";
      pythonStatus.value = "未知";
      rStatus.value = "未知";
      lastChecked.value = new Date();

      // 记录错误历史
      checkHistory.value.unshift({
        timestamp: lastChecked.value.toISOString(),
        status: {
          main: mainStatus.value,
          python: pythonStatus.value,
          r: rStatus.value,
        },
        changed: true,
        error: error.message,
      });

      if (checkHistory.value.length > 50) {
        checkHistory.value.pop();
      }

      throw error;
    } finally {
      loading.value = false;
    }
  };

  const startAutoCheck = (interval = 30000) => {
    // 清除已有的定时器
    if (autoCheckTimer.value) {
      clearInterval(autoCheckTimer.value);
    }

    // 立即检查一次
    checkServices();

    // 设置定时检查
    autoCheckTimer.value = setInterval(() => {
      checkServices();
    }, interval);

    return () => {
      if (autoCheckTimer.value) {
        clearInterval(autoCheckTimer.value);
        autoCheckTimer.value = null;
      }
    };
  };

  const stopAutoCheck = () => {
    if (autoCheckTimer.value) {
      clearInterval(autoCheckTimer.value);
      autoCheckTimer.value = null;
    }
  };

  const getCheckHistory = (limit = 10) => {
    return checkHistory.value.slice(0, limit);
  };

  const clearHistory = () => {
    checkHistory.value = [];
  };

  const getServiceStatus = () => {
    return {
      main: mainStatus.value,
      python: pythonStatus.value,
      r: rStatus.value,
      lastChecked: lastChecked.value,
      allHealthy: allServicesHealthy.value,
    };
  };

  const reset = () => {
    mainStatus.value = "检查中...";
    pythonStatus.value = "检查中...";
    rStatus.value = "检查中...";
    loading.value = false;
    lastChecked.value = null;
    stopAutoCheck();
  };

  const exportState = () => {
    return {
      mainStatus: mainStatus.value,
      pythonStatus: pythonStatus.value,
      rStatus: rStatus.value,
      lastChecked: lastChecked.value,
      checkHistory: checkHistory.value,
    };
  };

  const importState = (state) => {
    if (state.mainStatus) mainStatus.value = state.mainStatus;
    if (state.pythonStatus) pythonStatus.value = state.pythonStatus;
    if (state.rStatus) rStatus.value = state.rStatus;
    if (state.lastChecked) lastChecked.value = new Date(state.lastChecked);
    if (state.checkHistory) checkHistory.value = state.checkHistory;
  };

  // 清理定时器
  const dispose = () => {
    stopAutoCheck();
  };

  return {
    // 状态
    mainStatus,
    pythonStatus,
    rStatus,
    loading,
    lastChecked,
    checkHistory,

    // Getters
    allServicesHealthy,
    hasUnhealthyServices,
    formattedLastChecked,

    // Actions
    checkServices,
    startAutoCheck,
    stopAutoCheck,
    getCheckHistory,
    clearHistory,
    getServiceStatus,
    reset,
    exportState,
    importState,
    dispose,
  };
});
