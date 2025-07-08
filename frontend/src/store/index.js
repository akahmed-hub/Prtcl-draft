import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import protocolReducer from './slices/protocolSlice';
import analysisReducer from './slices/analysisSlice';
import visualizationReducer from './slices/visualizationSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    protocols: protocolReducer,
    analysis: analysisReducer,
    visualization: visualizationReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export default store; 