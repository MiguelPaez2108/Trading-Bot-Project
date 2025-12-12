# 🎯 RBI Process Checklist
## Research → Backtest → Implement

Este checklist debe seguirse **RELIGIOSAMENTE** antes de implementar cualquier estrategia de trading.

---

## 📚 FASE 1: RESEARCH (70% del tiempo total)

### 1.1 Investigación Académica
- [ ] Buscar papers en Google Scholar sobre la estrategia
- [ ] Leer al menos 3 papers académicos relacionados
- [ ] Documentar hallazgos clave en `notebooks/research/`
- [ ] Identificar edge teórico de la estrategia

### 1.2 Análisis de Mercado
- [ ] Identificar régimen de mercado actual
- [ ] Analizar correlaciones entre activos
- [ ] Estudiar microestructura del mercado objetivo
- [ ] Documentar condiciones ideales para la estrategia

### 1.3 Generación de Ideas
- [ ] Brainstorm de variaciones de la estrategia
- [ ] Identificar parámetros clave a optimizar
- [ ] Definir hipótesis falsables
- [ ] Crear documento de diseño de estrategia

### 1.4 Validación Conceptual
- [ ] Verificar que la estrategia tiene sentido económico
- [ ] Confirmar que no viola principios de no-arbitraje
- [ ] Revisar con otros traders/investigadores
- [ ] Documentar riesgos potenciales

---

## 🧪 FASE 2: BACKTEST (25% del tiempo total)

### 2.1 Preparación de Datos
- [ ] Descargar datos históricos (mínimo 2 años)
- [ ] Validar calidad de datos (gaps, outliers)
- [ ] Verificar survivorship bias
- [ ] Preparar datos out-of-sample (30% del total)

### 2.2 Implementación Inicial
- [ ] Implementar estrategia en `backtesting.py`
- [ ] Añadir logging detallado
- [ ] Implementar métricas de performance
- [ ] Crear tests unitarios

### 2.3 Backtesting Multi-Símbolo
- [ ] **CRÍTICO**: Testear en mínimo 5 símbolos diferentes
- [ ] Testear en diferentes timeframes (1h, 4h, 1d)
- [ ] Documentar resultados por símbolo
- [ ] Identificar símbolos con mejor performance

### 2.4 Optimización de Parámetros
- [ ] Definir rangos razonables para parámetros
- [ ] Ejecutar grid search
- [ ] Ejecutar walk-forward optimization
- [ ] Crear heat maps de resultados
- [ ] Verificar robustez (parámetros no deben ser muy sensibles)

### 2.5 Validación Out-of-Sample
- [ ] Testear en datos OOS (30% reservado)
- [ ] Comparar métricas in-sample vs out-of-sample
- [ ] Verificar que no hay overfitting
- [ ] Documentar degradación de performance (si existe)

### 2.6 Análisis de Riesgo
- [ ] Calcular Maximum Drawdown
- [ ] Calcular Sharpe Ratio (objetivo: >1.5)
- [ ] Calcular Sortino Ratio
- [ ] Calcular Calmar Ratio
- [ ] Analizar distribución de retornos
- [ ] Identificar peores períodos

### 2.7 Simulación Realista
- [ ] Incluir comisiones realistas (maker/taker)
- [ ] Incluir slippage estimado
- [ ] Simular latencia de ejecución
- [ ] Testear con diferentes tamaños de capital

### 2.8 Monte Carlo
- [ ] Ejecutar 1000+ simulaciones Monte Carlo
- [ ] Analizar percentiles de resultados (P5, P50, P95)
- [ ] Verificar probabilidad de ruina
- [ ] Documentar escenarios extremos

### 2.9 Criterios de Aprobación
- [ ] **Win Rate**: ≥ 45% (para estrategias direccionales)
- [ ] **Profit Factor**: ≥ 1.5
- [ ] **Sharpe Ratio**: ≥ 1.5
- [ ] **Max Drawdown**: ≤ 20%
- [ ] **Consistencia**: Positivo en ≥70% de los meses
- [ ] **Multi-símbolo**: Funciona en ≥3 símbolos diferentes

### 2.10 Documentación
- [ ] Crear notebook con análisis completo
- [ ] Documentar todos los parámetros optimizados
- [ ] Crear gráficos de equity curve
- [ ] Documentar trades de ejemplo (buenos y malos)
- [ ] Crear reporte ejecutivo

---

## 🚀 FASE 3: IMPLEMENT (5% del tiempo total)

### 3.1 Pre-Implementación
- [ ] Revisar checklist de RESEARCH y BACKTEST (100% completo)
- [ ] Obtener aprobación de resultados de backtest
- [ ] Definir plan de rollout gradual
- [ ] Preparar plan de contingencia

### 3.2 Implementación
- [ ] Implementar estrategia en código de producción
- [ ] Añadir todos los checks de riesgo
- [ ] Configurar alertas
- [ ] Crear dashboard de monitoreo

### 3.3 Paper Trading
- [ ] Ejecutar en paper trading por mínimo 1 semana
- [ ] Verificar que órdenes se ejecutan correctamente
- [ ] Monitorear latencia
- [ ] Comparar resultados con backtest

### 3.4 Live Trading - Fase 1 (TINY SIZE)
- [ ] **Empezar con $10-$50 de capital**
- [ ] Ejecutar por mínimo 2 semanas
- [ ] Monitorear 24/7
- [ ] Documentar todas las trades
- [ ] Verificar que performance es similar a backtest

### 3.5 Live Trading - Fase 2 (SMALL SIZE)
- [ ] Si Fase 1 exitosa, escalar a $100-$500
- [ ] Ejecutar por mínimo 1 mes
- [ ] Continuar monitoreo intensivo
- [ ] Ajustar parámetros si es necesario

### 3.6 Live Trading - Fase 3 (MEDIUM SIZE)
- [ ] Si Fase 2 exitosa, escalar a $1,000-$5,000
- [ ] Ejecutar por mínimo 2 meses
- [ ] Analizar performance mensual
- [ ] Optimizar gestión de riesgo

### 3.7 Live Trading - Fase 4 (FULL SIZE)
- [ ] Solo después de 3+ meses exitosos
- [ ] Escalar gradualmente hasta capital objetivo
- [ ] Mantener monitoreo continuo
- [ ] Re-optimizar cada trimestre

---

## ⚠️ CRITERIOS DE STOP

### Detener Inmediatamente Si:
- [ ] Drawdown > 15% en live trading
- [ ] 5 trades perdedores consecutivos
- [ ] Performance significativamente peor que backtest (>30% degradación)
- [ ] Cambio fundamental en condiciones de mercado
- [ ] Problemas técnicos recurrentes

### Revisar y Ajustar Si:
- [ ] Win rate < 40% por 2 semanas
- [ ] Sharpe ratio < 1.0 por 1 mes
- [ ] Slippage > 0.5% consistentemente
- [ ] Latencia > 500ms consistentemente

---

## 📊 MÉTRICAS DE SEGUIMIENTO

### Diarias
- [ ] P&L diario
- [ ] Número de trades
- [ ] Win rate
- [ ] Drawdown actual

### Semanales
- [ ] Sharpe ratio rolling
- [ ] Profit factor
- [ ] Average win/loss
- [ ] Comparación con backtest

### Mensuales
- [ ] Performance mensual
- [ ] Análisis de trades
- [ ] Optimización de parámetros
- [ ] Reporte ejecutivo

---

## ✅ APROBACIÓN FINAL

**Antes de pasar a producción, verificar:**

- [ ] ✅ Fase de RESEARCH 100% completa
- [ ] ✅ Fase de BACKTEST 100% completa
- [ ] ✅ Todas las métricas cumplen criterios mínimos
- [ ] ✅ Paper trading exitoso por ≥1 semana
- [ ] ✅ Plan de rollout gradual definido
- [ ] ✅ Sistema de monitoreo configurado
- [ ] ✅ Alertas configuradas
- [ ] ✅ Plan de contingencia documentado

**Firma de Aprobación**: _________________  
**Fecha**: _________________

---

> ⚠️ **RECORDATORIO CRÍTICO**: Si saltas algún paso de este checklist, estás aumentando dramáticamente tu probabilidad de pérdidas. El trading algorítmico exitoso requiere DISCIPLINA y PACIENCIA.
