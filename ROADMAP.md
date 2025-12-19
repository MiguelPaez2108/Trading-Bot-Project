# 🎯 ROADMAP ULTRA-DETALLADO COMPLETO Y CORREGIDO

Tienes razón, me faltaron componentes **CRÍTICOS** para un sistema production-ready. Voy a reorganizar el roadmap completo con **todas** las piezas faltantes.

---

## 📊 NUEVA VISIÓN GENERAL DEL ROADMAP (COMPLETA)

```
FASE 0: Setup & Foundation (3-5 días)
   ↓
FASE 1: RBI PROCESS FOUNDATION (1 semana) ⭐ NUEVA - OBLIGATORIA
   ↓
FASE 2: Core Infrastructure (1-2 semanas)
   ↓
FASE 3: Market Data Engine (1 semana)
   ↓
FASE 4: Backtesting System (2 semanas) ⭐ EXPANDIDA
   ↓
FASE 5: Risk Management (1 semana) ⭐ ANTES DEL EXECUTION
   ↓
FASE 6: Order Execution Engine (1 semana)
   ↓
FASE 7: Strategy Framework (1 semana)
   ↓
FASE 8: Scanner System (1 semana)
   ↓
FASE 9: APIs (Internal & External) (1 semana) ⭐ NUEVA
   ↓
FASE 10: Monitoring & Observability (1 semana) ⭐ EXPANDIDA
   ↓
FASE 11: DevOps & Infrastructure (1 semana) ⭐ NUEVA
   ↓
FASE 12: Testing Strategy (1 semana) ⭐ NUEVA
   ↓
FASE 13: Production Hardening (1 semana)
   ↓
FASE 14: Advanced Features (ongoing)
```

**Total estimado MVP**: 10-12 semanas  
**Total Production-Ready**: 14-16 semanas

---

## 🎯 FASE 1: RBI PROCESS FOUNDATION (Semana 1) ⭐ NUEVA - OBLIGATORIA

### **Sprint 1.1: Research Infrastructure**
**Duración**: 3 días

#### Contexto:
**NUNCA** empezar a codear sin research. El 70% del tiempo debe ir aquí.

#### Tareas:

##### 1. **Research Framework Setup** (`notebooks/research/`)
```python
# notebooks/research/strategy_research_template.ipynb

"""
TEMPLATE: Strategy Research Notebook

Sections:
1. Hypothesis
2. Literature Review
3. Data Exploration
4. Statistical Analysis
5. Initial Backtesting
6. Conclusion
"""

# 1. HYPOTHESIS
"""
Strategy: Breakout Strategy
Hypothesis: 
- Price breaking above 20-day resistance signals continuation
- Works best in trending markets
- Requires volume confirmation

Theoretical Basis:
- Support/Resistance theory
- Momentum continuation
- Market microstructure

Expected Edge:
- Catch strong trends early
- Risk/Reward ratio > 2:1
"""

# 2. LITERATURE REVIEW
papers_reviewed = [
    {
        'title': 'Momentum Strategies in Stock Markets',
        'authors': 'Jegadeesh and Titman (1993)',
        'key_findings': '...',
        'relevance': '...'
    },
    # ...
]

# 3. DATA EXPLORATION
import pandas as pd
import matplotlib.pyplot as plt

# Load historical data
data = pd.read_csv('data/historical/BTCUSDT_1d.csv')

# Exploratory analysis
print(data.describe())
print(data.isnull().sum())

# Visualize
plt.figure(figsize=(15, 10))
plt.subplot(3, 1, 1)
plt.plot(data['close'])
plt.title('Price History')
# ...
```

##### 2. **Research Checklist** (`docs/research/RESEARCH_CHECKLIST.md`)
```markdown
# Research Checklist

## ✅ Strategy Selection
- [ ] Strategy type defined (momentum/mean-reversion/arbitrage/etc)
- [ ] Theoretical basis documented
- [ ] Expected edge articulated
- [ ] Risk factors identified
- [ ] Market regime requirements defined

## ✅ Literature Review (MANDATORY)
- [ ] 5+ academic papers reviewed
- [ ] Key findings documented
- [ ] Contradicting evidence noted
- [ ] Similar strategies analyzed

### Papers to Review:
- Google Scholar: [link]
- SSRN: [link]
- ArXiv: [link]

### Books to Consult:
- [ ] "Advances in Financial Machine Learning" - Marcos López de Prado
- [ ] "Algorithmic Trading" - Ernest Chan
- [ ] "Evidence-Based Technical Analysis" - David Aronson

## ✅ Market Regime Analysis
- [ ] Identify in which regimes strategy should work
- [ ] Identify in which regimes strategy will FAIL
- [ ] Define regime detection criteria

Market Regimes (Jim Simons - 8 types):
1. Bull Market (trending up)
2. Bear Market (trending down)
3. Range-bound (sideways)
4. High Volatility
5. Low Volatility
6. Economic Boom
7. Economic Recession
8. Crisis

## ✅ Data Requirements
- [ ] Symbols needed: [list]
- [ ] Timeframes needed: [list]
- [ ] Historical period: [X years]
- [ ] Data sources identified
- [ ] Data quality requirements defined

## ✅ Risk Analysis
- [ ] Maximum theoretical loss calculated
- [ ] Black swan scenarios identified
- [ ] Correlation risks documented
- [ ] Liquidity risks assessed

## ✅ Hypothesis Document
- [ ] Clear hypothesis statement
- [ ] Testable predictions
- [ ] Success criteria defined
- [ ] Failure criteria defined
```

##### 3. **Data Collection Scripts** (`scripts/research/`)
```python
# scripts/research/collect_research_data.py

import ccxt
import pandas as pd
from pathlib import Path
import asyncio
from datetime import datetime, timedelta

class ResearchDataCollector:
    """
    Collect data for research phase.
    
    Requirements:
    - Multiple symbols
    - Multiple timeframes
    - Long history (2+ years)
    - High quality (no gaps)
    """
    
    def __init__(self, exchange_id: str = 'binance'):
        self.exchange = getattr(ccxt, exchange_id)({
            'enableRateLimit': True
        })
        self.data_dir = Path('data/research')
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def collect_for_research(
        self,
        symbols: list,
        timeframes: list,
        start_date: str,
        end_date: str = None
    ):
        """
        Collect comprehensive dataset for research.
        
        Args:
            symbols: ['BTC/USDT', 'ETH/USDT', ...]
            timeframes: ['1d', '4h', '1h']
            start_date: '2022-01-01'
            end_date: '2024-12-01' (optional)
        """
        print(f"🔍 Collecting research data...")
        print(f"Symbols: {len(symbols)}")
        print(f"Timeframes: {timeframes}")
        print(f"Date range: {start_date} to {end_date or 'now'}")
        
        for symbol in symbols:
            for timeframe in timeframes:
                print(f"\n📊 Downloading {symbol} {timeframe}...")
                
                try:
                    # Download OHLCV
                    ohlcv = await self._download_ohlcv(
                        symbol=symbol,
                        timeframe=timeframe,
                        since=self._parse_date(start_date),
                        until=self._parse_date(end_date) if end_date else None
                    )
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(
                        ohlcv,
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
                    )
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                    
                    # Validate
                    self._validate_data(df, symbol, timeframe)
                    
                    # Save
                    filename = f"{symbol.replace('/', '')}_{timeframe}.csv"
                    filepath = self.data_dir / filename
                    df.to_csv(filepath, index=False)
                    
                    print(f"✅ Saved {len(df)} candles to {filepath}")
                    
                except Exception as e:
                    print(f"❌ Error downloading {symbol} {timeframe}: {e}")
    
    def _validate_data(self, df: pd.DataFrame, symbol: str, timeframe: str):
        """
        Validate data quality.
        
        Checks:
        - No gaps
        - No nulls
        - Price sanity
        - Volume sanity
        """
        # Check nulls
        nulls = df.isnull().sum()
        if nulls.any():
            print(f"⚠️  Warning: Found nulls in {symbol} {timeframe}")
            print(nulls[nulls > 0])
        
        # Check gaps (assuming regular intervals)
        df_sorted = df.sort_values('timestamp')
        time_diffs = df_sorted['timestamp'].diff()
        
        # Expected interval
        intervals = {
            '1m': timedelta(minutes=1),
            '5m': timedelta(minutes=5),
            '15m': timedelta(minutes=15),
            '1h': timedelta(hours=1),
            '4h': timedelta(hours=4),
            '1d': timedelta(days=1)
        }
        expected_interval = intervals.get(timeframe)
        
        if expected_interval:
            gaps = time_diffs[time_diffs > expected_interval * 1.5]
            if not gaps.empty:
                print(f"⚠️  Warning: Found {len(gaps)} gaps in {symbol} {timeframe}")
        
        # Price sanity (no zeros, no negatives)
        if (df[['open', 'high', 'low', 'close']] <= 0).any().any():
            print(f"❌ ERROR: Found invalid prices in {symbol} {timeframe}")
        
        # Volume sanity
        if (df['volume'] < 0).any():
            print(f"❌ ERROR: Found negative volume in {symbol} {timeframe}")
        
        print(f"✅ Data validation passed for {symbol} {timeframe}")

# Usage
if __name__ == '__main__':
    collector = ResearchDataCollector()
    
    # Research dataset
    symbols = [
        'BTC/USDT',
        'ETH/USDT',
        'SOL/USDT',
        'AVAX/USDT',
        'MATIC/USDT'
    ]
    
    timeframes = ['1d', '4h', '1h']
    
    asyncio.run(
        collector.collect_for_research(
            symbols=symbols,
            timeframes=timeframes,
            start_date='2022-01-01'
        )
    )
```

##### 4. **Strategy Hypothesis Document Template** (`docs/research/HYPOTHESIS_TEMPLATE.md`)
```markdown
# Strategy Hypothesis Document

## Basic Information
- **Strategy Name**: Breakout Strategy
- **Strategy Type**: Momentum
- **Author**: [Your Name]
- **Date**: 2024-01-15
- **Status**: Research Phase

---

## 1. Hypothesis Statement

### Primary Hypothesis
When price closes above the 20-day high (resistance) on increased volume, 
it signals the beginning of a momentum move that will continue for 
3-7 days with high probability.

### Testable Predictions
1. Win rate will be >45% across multiple assets
2. Average winner will be >2x average loser (reward/risk > 2:1)
3. Strategy will outperform buy-and-hold by 50%+ in trending markets
4. Strategy will underperform in range-bound markets

---

## 2. Theoretical Basis

### Market Dynamics
- **Support/Resistance Theory**: Price levels act as barriers
- **Breakout Psychology**: Breaking resistance signals strength
- **Momentum Continuation**: Trends persist more than they reverse

### Academic Support
Papers supporting this approach:
1. Jegadeesh & Titman (1993) - "Returns to Buying Winners"
2. Chan, Jegadeesh & Lakonishok (1996) - "Momentum Strategies"
3. [Add more]

### Contradicting Evidence
Papers showing limitations:
1. Daniel & Moskowitz (2016) - "Momentum Crashes"
2. [Add more]

---

## 3. Market Regime Requirements

### Optimal Regimes
✅ Bull Market (strong trending up)
✅ High Volatility (with trend)
✅ Economic Boom

### Suboptimal Regimes
⚠️ Range-bound (will generate false signals)
❌ Bear Market (breakouts often fail)
❌ Crisis (extreme volatility)

### Regime Detection
We will detect regimes using:
- 200-day SMA slope (trend)
- ATR/Price ratio (volatility)
- Market breadth indicators

---

## 4. Risk Factors

### Identified Risks
1. **False Breakouts**: Price breaks resistance but immediately reverses
   - Mitigation: Volume confirmation, ATR filter
   
2. **Whipsaw in Range-bound**: Multiple failed breakouts
   - Mitigation: Regime filter, reduce position size
   
3. **Gap Risk**: Price gaps down overnight
   - Mitigation: Crypto markets (24/7), stop losses
   
4. **Liquidity Risk**: Slippage on entry/exit
   - Mitigation: Minimum volume filter ($1M+ daily)

### Maximum Theoretical Loss
- Single trade: -16% (stop loss)
- Daily: -5% (circuit breaker)
- Monthly: -15% (risk limit)

### Black Swan Scenarios
1. Flash crash: Stop loss slippage >50%
2. Exchange hack: All funds lost
3. Regulatory ban: Assets frozen

---

## 5. Data Requirements

### Symbols
Primary: BTC/USDT, ETH/USDT, SOL/USDT
Secondary: 20+ altcoins for validation

### Timeframes
- Daily (for resistance calculation)
- Hourly (for entry timing)
- 5-minute (optional: for stop loss management)

### Historical Period
Minimum: 2 years
Ideal: 3-5 years

### Data Quality Requirements
- No gaps >1 day
- Volume data accurate
- Price data validated (no outliers)

---

## 6. Success Criteria

### Backtest Phase
✅ Sharpe Ratio > 1.0
✅ Max Drawdown < 30%
✅ Win Rate > 40%
✅ Profit Factor > 1.5
✅ Works on 5+ symbols
✅ Works on 3+ time periods (walk-forward)

### Paper Trading Phase
✅ Results within 10% of backtest
✅ No technical failures
✅ Execution latency <100ms

### Live Trading Phase (Tiny Size)
✅ Positive P&L after 30 days
✅ No violations of risk limits
✅ System uptime >99%

---

## 7. Failure Criteria

### Backtest Phase
❌ Sharpe Ratio < 0.5
❌ Max Drawdown > 40%
❌ Win Rate < 30%
❌ Only works on 1-2 symbols (overfitting)
❌ Fails in walk-forward test

### Live Trading Phase
❌ Drawdown exceeds backtest by >50%
❌ Multiple technical failures
❌ Negative P&L for 2 consecutive months

### Action on Failure
1. Stop trading immediately
2. Analyze failure reasons
3. Return to research phase
4. Modify or abandon strategy

---

## 8. Next Steps

### Research Phase (Week 1-2)
- [ ] Review 5+ academic papers
- [ ] Analyze historical market regimes
- [ ] Document all findings
- [ ] Create initial hypothesis

### Data Collection (Week 2)
- [ ] Download 3+ years of data
- [ ] Validate data quality
- [ ] Create research database

### Initial Analysis (Week 3)
- [ ] Exploratory data analysis
- [ ] Statistical tests
- [ ] Correlation analysis
- [ ] Regime classification

### Proceed to Backtest Phase
Only if:
✅ Hypothesis is clear and testable
✅ Data is complete and validated
✅ Risk factors are documented
✅ Success/failure criteria defined
```

### **Criterios de Aceptación**:
- ✅ Research framework setup completo
- ✅ Hypothesis document created para strategy
- ✅ 3+ años de data descargada y validada
- ✅ 5+ papers académicos revisados
- ✅ Risk factors documentados
- ✅ Success criteria definidos claramente

### **Entregables**:
- Jupyter notebooks para research
- Research checklist completado
- Data collection scripts
- Hypothesis document para breakout strategy
- Literature review document
- Risk analysis document

---

### **Sprint 1.2: Backtesting Requirements**
**Duración**: 2 días

#### Tareas:

##### 1. **Backtesting Checklist** (`docs/backtesting/BACKTEST_CHECKLIST.md`)
```markdown
# Backtesting Checklist

## ✅ Pre-Backtest Setup

### Data Preparation
- [ ] Historical data downloaded (min 2 years)
- [ ] Data validated (no gaps, no errors)
- [ ] Data covers multiple market regimes
- [ ] Out-of-sample period reserved (20% of data)

### Commission Model
- [ ] Maker fees configured (usually 0.02-0.1%)
- [ ] Taker fees configured (usually 0.04-0.2%)
- [ ] Model matches target exchange
- [ ] Fee tiers considered (if volume-based)

### Slippage Model
- [ ] Slippage model selected (fixed/dynamic)
- [ ] Model calibrated to market conditions
- [ ] Higher slippage for market orders
- [ ] Lower slippage for limit orders

### Market Impact Model (optional for HFT)
- [ ] Impact model for large orders
- [ ] Orderbook depth considered

---

## ✅ Initial Backtest

### Single Symbol Test
- [ ] Strategy coded in backtesting.py
- [ ] Run on primary symbol (e.g., BTC/USDT)
- [ ] Results documented
- [ ] Equity curve reviewed
- [ ] Drawdown analyzed

### Key Metrics
```
Target Metrics:
- Sharpe Ratio: > 1.0
- Sortino Ratio: > 1.5
- Max Drawdown: < 30%
- Win Rate: > 40%
- Profit Factor: > 1.5
- Calmar Ratio: > 1.0
```

### Trade Analysis
- [ ] Avg winner vs avg loser calculated
- [ ] Trade duration analyzed
- [ ] Entry/exit timing reviewed
- [ ] Slippage impact assessed

---

## ✅ Multi-Symbol Validation

### Test on 5+ Symbols
1. [ ] BTC/USDT
2. [ ] ETH/USDT
3. [ ] SOL/USDT
4. [ ] AVAX/USDT
5. [ ] MATIC/USDT
6. [ ] [Add more]

### Consistency Check
- [ ] Strategy works on >60% of symbols
- [ ] Performance is consistent (not 1 outlier)
- [ ] Risk metrics similar across symbols

### Survivorship Bias Check
- [ ] Test includes delisted tokens (if applicable)
- [ ] Results don't rely on "token that mooned"
- [ ] Conservative symbol selection

---

## ✅ Parameter Optimization

### Grid Search
- [ ] Parameter ranges defined
- [ ] Grid search executed (100+ combinations)
- [ ] Heat map generated
- [ ] Optimal parameters identified

### Overfitting Prevention
- [ ] In-sample period: 60-70% of data
- [ ] Out-of-sample period: 20-30% of data
- [ ] Test set: 10% (untouched until final validation)
- [ ] Performance similar IS vs OOS

### Walk-Forward Optimization
- [ ] Multiple train/test windows (5+)
- [ ] Rolling window approach
- [ ] Results stable across windows
- [ ] No parameter drift over time

---

## ✅ Regime-Specific Testing

### Test in Different Regimes
- [ ] Bull market period
- [ ] Bear market period
- [ ] Range-bound period
- [ ] High volatility period
- [ ] Low volatility period

### Regime Performance
```
Expected Results:
- Bull Market: Strong performance
- Bear Market: Break-even or small loss
- Range-bound: Underperform or stop trading
```

### Regime Filter (if needed)
- [ ] Add regime detection
- [ ] Only trade in favorable regimes
- [ ] Results improve with filter

---

## ✅ Risk Analysis

### Drawdown Analysis
- [ ] Maximum drawdown < 30%
- [ ] Average drawdown < 15%
- [ ] Recovery time < 30 days
- [ ] Underwater periods documented

### Tail Risk
- [ ] 95th percentile loss calculated
- [ ] 99th percentile loss calculated
- [ ] Worst day documented
- [ ] Worst week documented

### Monte Carlo Simulation
- [ ] 1000+ simulations run
- [ ] Confidence intervals calculated
- [ ] Worst-case scenario documented
- [ ] Probability of ruin < 1%

---

## ✅ Validation Tests

### Out-of-Sample Test
- [ ] Strategy tested on unseen data
- [ ] Performance within 20% of in-sample
- [ ] Sharpe ratio > 0.8
- [ ] No catastrophic failures

### Time-Period Test
- [ ] Test on 2022 (crypto winter)
- [ ] Test on 2023 (recovery)
- [ ] Test on 2024 (bull market)
- [ ] Consistent across periods

### Sensitivity Analysis
- [ ] Test with +10% commission
- [ ] Test with +50% slippage
- [ ] Test with +20% volatility
- [ ] Strategy still profitable

---

## ✅ Final Validation

### Acceptance Criteria Met
- [ ] All metrics above thresholds
- [ ] Works on multiple symbols
- [ ] Works in multiple regimes
- [ ] Survives stress tests
- [ ] OOS performance good

### Documentation Complete
- [ ] Backtest report generated
- [ ] All metrics documented
- [ ] Charts/plots saved
- [ ] Known limitations listed

### Proceed to Implementation
Only if:
✅ All checkboxes above are checked
✅ Team reviewed and approved
✅ Risk team signed off
✅ Hypothesis validated

---

## 🚨 Red Flags (STOP)

❌ Sharpe < 0.5 in backtest
❌ Works only on 1-2 symbols (overfitting)
❌ OOS performance <50% of IS performance
❌ Max drawdown > 40%
❌ Strategy fails in any tested regime
❌ Too good to be true (Sharpe > 3, no drawdowns)

If any red flag → STOP, return to research phase
```

##### 2. **Backtest Configuration Template** (`config/backtest_config.yaml`)
```yaml
# Backtest Configuration Template

backtest:
  name: "breakout_strategy_initial"
  description: "Initial backtest of breakout strategy"
  
  # Data
  data:
    symbols:
      - "BTC/USDT"
      - "ETH/USDT"
      - "SOL/USDT"
    timeframe: "1h"
    start_date: "2022-01-01"
    end_date: "2024-12-01"
    
    # Data splits
    in_sample:
      start: "2022-01-01"
      end: "2023-12-31"
    out_of_sample:
      start: "2024-01-01"
      end: "2024-12-01"
  
  # Capital
  initial_capital: 10000
  currency: "USDT"
  
  # Commission
  commission:
    maker: 0.0002  # 0.02%
    taker: 0.0004  # 0.04%
    model: "tiered"  # fixed, tiered, dynamic
  
  # Slippage
  slippage:
    model: "dynamic"  # fixed, dynamic, orderbook
    market_order: 0.001  # 0.1%
    limit_order: 0.0005  # 0.05%
  
  # Strategy parameters
  strategy:
    name: "BreakoutStrategy"
    parameters:
      lookback_days: 20
      tp_percent: 0.07  # 7%
      sl_percent: 0.16  # 16%
      min_volume_usd: 1000000
  
  # Risk limits
  risk:
    max_position_size: 0.1  # 10% of capital per trade
    max_positions: 3
    max_leverage: 1  # No leverage in backtest
    
  # Optimization (if running optimization)
  optimization:
    enabled: false
    method: "grid_search"  # grid_search, walk_forward, genetic
    parameters:
      lookback_days: [10, 15, 20, 25, 30]
      tp_percent: [0.03, 0.05, 0.07, 0.10, 0.15, 0.20]
      sl_percent: [0.05, 0.10, 0.15, 0.20]
    objective: "sharpe_ratio"  # sharpe_ratio, sortino, calmar, profit_factor
  
  # Walk-forward (if enabled)
  walk_forward:
    enabled: false
    train_period_days: 180  # 6 months
    test_period_days: 60    # 2 months
    step_days: 30           # Re-optimize every month
  
  # Output
  output:
    save_trades: true
    save_equity_curve: true
    save_plots: true
    generate_report: true
    output_dir: "data/backtests/breakout_initial"
```

##### 3. **Backtest Runner Script** (`scripts/run_backtest.py`)
```python
# scripts/run_backtest.py

import yaml
import pandas as pd
from pathlib import Path
from backtesting import Backtest
from rich.console import Console
from rich.table import Table

from src.python.strategies.momentum.breakout import BreakoutStrategy
from src.python.backtesting.metrics import calculate_all_metrics
from src.python.backtesting.reports import generate_html_report

console = Console()

class BacktestRunner:
    """
    Run backtests with configuration.
    """
    
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.output_dir = Path(self.config['backtest']['output']['output_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self):
        """
        Run backtest based on configuration.
        """
        console.print(f"\n🚀 Running backtest: {self.config['backtest']['name']}", style="bold cyan")
        
        # Load data
        data = self._load_data()
        
        # Run on each symbol
        results = {}
        for symbol in self.config['backtest']['data']['symbols']:
            console.print(f"\n📊 Testing {symbol}...", style="yellow")
            
            symbol_data = data[symbol]
            result = self._run_single_backtest(symbol, symbol_data)
            results[symbol] = result
            
            self._print_results(symbol, result)
        
        # Aggregate results
        self._aggregate_results(results)
        
        # Generate reports
        if self.config['backtest']['output']['generate_report']:
            self._generate_reports(results)
        
        console.print("\n✅ Backtest complete!", style="bold green")
    
    def _run_single_backtest(self, symbol: str, data: pd.DataFrame):
        """
        Run backtest on single symbol.
        """
        # Setup strategy
        strategy_config = self.config['backtest']['strategy']
        
        # Create backtest
        bt = Backtest(
            data,
            BreakoutStrategy,
            cash=self.config['backtest']['initial_capital'],
            commission=self.config['backtest']['commission']['taker'],
            exclusive_orders=True
        )
        
        # Run
        stats = bt.run(**strategy_config['parameters'])
        
        # Calculate additional metrics
        trades_df = stats['_trades']
        metrics = calculate_all_metrics(
            equity_curve=stats['_equity_curve'],
            trades=trades_df,
            initial_capital=self.config['backtest']['initial_capital']
        )
        
        return {
            'stats': stats,
            'metrics': metrics,
            'trades': trades_df,
            'backtest_obj': bt
        }
    
    def _print_results(self, symbol: str, result: dict):
        """
        Print results in nice table.
        """
        metrics = result['metrics']
        
        table = Table(title=f"Results: {symbol}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Total Return", f"{metrics['total_return']:.2%}")
        table.add_row("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
        table.add_row("Sortino Ratio", f"{metrics['sortino_ratio']:.2f}")
        table.add_row("Max Drawdown", f"{metrics['max_drawdown']:.2%}")
        table.add_row("Win Rate", f"{metrics['win_rate']:.2%}")
        table.add_row("Profit Factor", f"{metrics['profit_factor']:.2f}")
        table.add_row("# Trades", str(metrics['num_trades']))
        
        console.print(table)
    
    def _aggregate_results(self, results: dict):
        """
        Aggregate results across symbols.
        """
        console.print("\n📈 Aggregate Results", style="bold cyan")
        
        # Calculate averages
        avg_sharpe = sum(r['metrics']['sharpe_ratio'] for r in results.values()) / len(results)
        avg_return = sum(r['metrics']['total_return'] for r in results.values()) / len(results)
        avg_drawdown = sum(r['metrics']['max_drawdown'] for r in results.values()) / len(results)
        
        symbols_profitable = sum(1 for r in results.values() if r['metrics']['total_return'] > 0)
        
        table = Table(title="Summary Across All Symbols")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Symbols Tested", str(len(results)))
        table.add_row("Symbols Profitable", f"{symbols_profitable}/{len(results)}")
        table.add_row("Avg Return", f"{avg_return:.2%}")
        table.add_row("Avg Sharpe", f"{avg_sharpe:.2f}")
        table.add_row("Avg Max DD", f"{avg_drawdown:.2%}")
        
        console.print(table)

# Usage
if __name__ == '__main__':
    runner = BacktestRunner('config/backtest_config.yaml')
    runner.run()
```

### **Criterios de Aceptación**:
- ✅ Backtest checklist completo
- ✅ Config template creado
- ✅ Backtest runner implementado
- ✅ Multi-symbol testing funciona
- ✅ Reports generados automáticamente

### **Entregables**:
- Backtest checklist document
- Configuration templates
- Backtest runner script
- Sample backtest results (on research data)
- Validation that strategy meets acceptance criteria

---

### **Sprint 1.3: Implementation Readiness**
**Duración**: 2 días

#### Tareas:

##### 1. **Implementation Checklist** (`docs/implementation/IMPLEMENTATION_CHECKLIST.md`)
```markdown
# Implementation Checklist

⚠️ **CRITICAL**: Only proceed to implementation if ALL items checked.

## ✅ Research Phase Complete
- [ ] Strategy hypothesis validated
- [ ] 5+ academic papers reviewed
- [ ] Risk factors documented
- [ ] Market regimes identified
- [ ] Data collected and validated

## ✅ Backtest Phase Complete
- [ ] Sharpe Ratio > 1.0
- [ ] Max Drawdown < 30%
- [ ] Win Rate > 40%
- [ ] Profit Factor > 1.5
- [ ] Works on 5+ symbols
- [ ] Walk-forward validation passed
- [ ] Out-of-sample test passed
- [ ] Survives stress tests

## ✅ Technical Infrastructure Ready
- [ ] Exchange connector working (testnet)
- [ ] Market data feed functional
- [ ] Database setup complete
- [ ] Risk management implemented
- [ ] Order execution tested
- [ ] Monitoring/alerting configured

## ✅ Risk Management Ready
- [ ] Position size limits configured
- [ ] Stop loss MANDATORY
- [ ] Take profit MANDATORY
- [ ] Daily loss limit set
- [ ] Circuit breakers implemented
- [ ] Duplicate order prevention tested

## ✅ Paper Trading Plan
- [ ] Paper trading duration: 1 week minimum
- [ ] Success criteria defined
- [ ] Failure criteria defined
- [ ] Monitoring plan in place

## ✅ Live Trading Plan (TINY SIZE)
```
Week 1: $10-20 per position
Week 2: $25-50 per position (if week 1 successful)
Week 3: $50-100 per position (if week 2 successful)
Week 4+: Scale based on results
```

- [ ] Initial position size: $10-20
- [ ] Scaling plan documented
- [ ] Emergency stop procedures defined

## ✅ Documentation Complete
- [ ] Strategy documentation written
- [ ] Risk documentation complete
- [ ] Runbook created (how to operate)
- [ ] Troubleshooting guide written
- [ ] Emergency procedures documented

---

## 🚨 Go/No-Go Decision

### GO if:
✅ ALL checkboxes above are checked
✅ Backtest Sharpe > 1.0
✅ Team consensus to proceed
✅ Risk team approval
✅ Starting with TINY size ($10-20)

### NO-GO if:
❌ Any checkbox unchecked
❌ Backtest performance marginal
❌ Technical issues unresolved
❌ Team not confident
❌ Trying to start with large size

---

## Implementation Phases

### Phase 1: Paper Trading (Week 1)
- Run strategy in simulation mode
- Monitor performance 4x daily
- Log all signals and executions
- Compare to backtest expectations

### Phase 2: Live Trading - Tiny Size (Week 2-4)
- Start with $10-20 positions
- Monitor CONSTANTLY (multiple times per day)
- Document every trade
- Scale SLOWLY based on results

### Phase 3: Scale Up (Month 2+)
- Only if Phase 1 and 2 successful
- Gradual size increases
- Continue monitoring closely
- Maintain detailed logs

---

## Success Criteria

### Paper Trading
✅ 90%+ of signals match backtest
✅ No technical failures
✅ Execution latency <100ms
✅ Risk checks functioning

### Live Trading (Month 1)
✅ Positive P&L (any amount)
✅ No stop loss failures
✅ No liquidations
✅ System uptime >99%
✅ Results within 20% of backtest

### Live Trading (Month 2-3)
✅ Sharpe ratio > 0.8
✅ Drawdown < backtest + 10%
✅ Win rate within 10% of backtest
✅ No major technical issues

---

## Failure Criteria & Actions

### Paper Trading Failure
❌ <70% of signals match backtest
→ Action: Debug, fix issues, restart paper trading

❌ Technical failures
→ Action: Fix issues, add more tests, restart

### Live Trading Failure
❌ Drawdown > 2x backtest
→ Action: STOP immediately, analyze, return to backtest

❌ Multiple stop loss failures
→ Action: STOP, fix execution, retest

❌ Negative P&L for 30 days
→ Action: Reduce size to minimum or pause

❌ System downtime >1%
→ Action: Fix reliability, don't scale

---

## Emergency Procedures

### If drawdown > 20%:
1. STOP trading immediately
2. Close all positions
3. Notify team
4. Analyze what went wrong
5. Don't resume until fixed

### If technical failure:
1. Close positions safely
2. Stop strategy
3. Fix issue
4. Test thoroughly
5. Resume slowly

### If exchange issues:
1. Check if exchange-wide or just you
2. Try to close positions
3. Contact exchange support
4. Don't open new positions until resolved

---

Remember: **The bot is the EASY part**. The hard part is research and validation.
```

### **Criterios de Aceptación**:
- ✅ Implementation checklist created
- ✅ Go/No-Go criteria defined
- ✅ Scaling plan documented
- ✅ Emergency procedures defined
- ✅ Success/failure criteria clear

### **Entregables**:
- Implementation checklist
- Paper trading plan
- Live trading plan (tiny size)
- Emergency procedures document
- Go/No-Go decision framework

---

## 🎯 RESUMEN FASE 1

Al completar la Fase 1, tendrás:

✅ **Research Framework** completo
✅ **Hypothesis Document** para tu estrategia
✅ **3+ años de data** descargada y validada
✅ **5+ papers académicos** revisados
✅ **Backtest Checklist** completo
✅ **Implementation Readiness** verificada
✅ **Go/No-Go criteria** definidos

**Tiempo total**: 1 semana (si trabajas full-time)

**Siguiente paso**: Solo si TODOS los criterios se cumplen → FASE 2: Core Infrastructure

# 🏗️ FASE 2: CORE INFRASTRUCTURE (Semana 2-3)

## **Sprint 2.1: Database Layer & Persistence**
**Duración**: 3-4 días

### Tareas:

#### 1. **TimescaleDB Setup & Schema** (`infrastructure/database/schema.sql`)
```sql
-- infrastructure/database/schema.sql

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- =====================================================
-- MARKET DATA TABLES
-- =====================================================

-- Candles (OHLCV) - Main hypertable
CREATE TABLE candles (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    open NUMERIC(20, 8) NOT NULL,
    high NUMERIC(20, 8) NOT NULL,
    low NUMERIC(20, 8) NOT NULL,
    close NUMERIC(20, 8) NOT NULL,
    volume NUMERIC(20, 8) NOT NULL,
    quote_volume NUMERIC(20, 8),
    trades_count INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Convert to hypertable
SELECT create_hypertable('candles', 'time', 
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

-- Create indexes
CREATE INDEX idx_candles_symbol_time ON candles (symbol, time DESC);
CREATE INDEX idx_candles_exchange_symbol ON candles (exchange, symbol, time DESC);
CREATE INDEX idx_candles_timeframe ON candles (timeframe, time DESC);

-- Compression policy (compress data older than 7 days)
ALTER TABLE candles SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol,exchange,timeframe'
);

SELECT add_compression_policy('candles', INTERVAL '7 days');

-- Retention policy (keep 2 years)
SELECT add_retention_policy('candles', INTERVAL '2 years');

-- Continuous aggregates for common timeframes
CREATE MATERIALIZED VIEW candles_15m
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('15 minutes', time) AS time,
    symbol,
    exchange,
    '15m' as timeframe,
    first(open, time) as open,
    max(high) as high,
    min(low) as low,
    last(close, time) as close,
    sum(volume) as volume,
    sum(quote_volume) as quote_volume,
    sum(trades_count) as trades_count
FROM candles
WHERE timeframe = '1m'
GROUP BY time_bucket('15 minutes', time), symbol, exchange;

-- Similar for 1h, 4h, 1d
-- (repeat pattern above)

-- =====================================================
-- TRADES TABLE (tick data)
-- =====================================================

CREATE TABLE trades (
    time TIMESTAMPTZ NOT NULL,
    trade_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    price NUMERIC(20, 8) NOT NULL,
    quantity NUMERIC(20, 8) NOT NULL,
    quote_quantity NUMERIC(20, 8),
    side TEXT NOT NULL, -- 'buy' or 'sell'
    is_buyer_maker BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('trades', 'time',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

CREATE INDEX idx_trades_symbol_time ON trades (symbol, time DESC);
CREATE UNIQUE INDEX idx_trades_unique ON trades (exchange, symbol, trade_id, time);

-- Compression
ALTER TABLE trades SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol,exchange'
);
SELECT add_compression_policy('trades', INTERVAL '3 days');

-- =====================================================
-- ORDERBOOK SNAPSHOTS
-- =====================================================

CREATE TABLE orderbook_snapshots (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    bids JSONB NOT NULL, -- Array of [price, quantity]
    asks JSONB NOT NULL,
    sequence_id BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('orderbook_snapshots', 'time',
    chunk_time_interval => INTERVAL '1 hour',
    if_not_exists => TRUE
);

CREATE INDEX idx_orderbook_symbol_time ON orderbook_snapshots (symbol, time DESC);

-- =====================================================
-- LIQUIDATIONS TABLE (NEW - Moon Dev feature)
-- =====================================================

CREATE TABLE liquidations (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    side TEXT NOT NULL, -- 'long' or 'short'
    price NUMERIC(20, 8) NOT NULL,
    quantity NUMERIC(20, 8) NOT NULL,
    quantity_usd NUMERIC(20, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('liquidations', 'time',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

CREATE INDEX idx_liquidations_symbol_time ON liquidations (symbol, time DESC);
CREATE INDEX idx_liquidations_size ON liquidations (quantity_usd DESC, time DESC);

-- Aggregated liquidations view (by price level)
CREATE MATERIALIZED VIEW liquidations_by_level
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('5 minutes', time) AS time,
    symbol,
    side,
    floor(price / 100) * 100 as price_level, -- Round to nearest 100
    sum(quantity_usd) as total_usd,
    count(*) as count
FROM liquidations
GROUP BY time_bucket('5 minutes', time), symbol, side, price_level;

-- =====================================================
-- ORDERS TABLE
-- =====================================================

CREATE TABLE orders (
    id TEXT PRIMARY KEY,
    client_order_id TEXT UNIQUE,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    side TEXT NOT NULL, -- 'buy' or 'sell'
    order_type TEXT NOT NULL, -- 'market', 'limit', 'stop_loss', etc.
    status TEXT NOT NULL, -- 'pending', 'filled', 'cancelled', 'rejected'
    price NUMERIC(20, 8),
    quantity NUMERIC(20, 8) NOT NULL,
    filled_quantity NUMERIC(20, 8) DEFAULT 0,
    average_fill_price NUMERIC(20, 8),
    stop_loss NUMERIC(20, 8),
    take_profit NUMERIC(20, 8),
    time_in_force TEXT DEFAULT 'GTC',
    reduce_only BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    filled_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ
);

CREATE INDEX idx_orders_symbol ON orders (symbol, created_at DESC);
CREATE INDEX idx_orders_status ON orders (status, created_at DESC);
CREATE INDEX idx_orders_exchange ON orders (exchange, symbol, created_at DESC);

-- =====================================================
-- TRADES TABLE (our executed trades)
-- =====================================================

CREATE TABLE executed_trades (
    id TEXT PRIMARY KEY,
    order_id TEXT REFERENCES orders(id),
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    side TEXT NOT NULL,
    price NUMERIC(20, 8) NOT NULL,
    quantity NUMERIC(20, 8) NOT NULL,
    commission NUMERIC(20, 8) NOT NULL,
    commission_asset TEXT,
    realized_pnl NUMERIC(20, 8),
    executed_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_executed_trades_order ON executed_trades (order_id);
CREATE INDEX idx_executed_trades_symbol ON executed_trades (symbol, executed_at DESC);

-- =====================================================
-- POSITIONS TABLE
-- =====================================================

CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    side TEXT NOT NULL, -- 'long' or 'short'
    quantity NUMERIC(20, 8) NOT NULL,
    entry_price NUMERIC(20, 8) NOT NULL,
    current_price NUMERIC(20, 8) NOT NULL,
    unrealized_pnl NUMERIC(20, 8),
    realized_pnl NUMERIC(20, 8) DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'open', -- 'open' or 'closed'
    stop_loss NUMERIC(20, 8),
    take_profit NUMERIC(20, 8),
    opened_at TIMESTAMPTZ NOT NULL,
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_positions_symbol_status ON positions (symbol, status);
CREATE INDEX idx_positions_exchange ON positions (exchange, symbol, status);
CREATE UNIQUE INDEX idx_positions_open ON positions (symbol, exchange, status) 
    WHERE status = 'open';

-- =====================================================
-- SIGNALS TABLE (trading signals generated)
-- =====================================================

CREATE TABLE signals (
    id SERIAL PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    signal_type TEXT NOT NULL, -- 'entry', 'exit', 'stop_loss', 'take_profit'
    side TEXT NOT NULL, -- 'buy' or 'sell'
    price NUMERIC(20, 8) NOT NULL,
    confidence NUMERIC(3, 2), -- 0.00 to 1.00
    stop_loss NUMERIC(20, 8),
    take_profit NUMERIC(20, 8),
    metadata JSONB,
    executed BOOLEAN DEFAULT FALSE,
    order_id TEXT REFERENCES orders(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_signals_strategy ON signals (strategy_name, created_at DESC);
CREATE INDEX idx_signals_symbol ON signals (symbol, created_at DESC);
CREATE INDEX idx_signals_executed ON signals (executed, created_at DESC);

-- =====================================================
-- SCANNER RESULTS TABLE (NEW)
-- =====================================================

CREATE TABLE scanner_results (
    id SERIAL PRIMARY KEY,
    scanner_name TEXT NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    entry_price NUMERIC(20, 8) NOT NULL,
    stop_loss NUMERIC(20, 8),
    take_profit NUMERIC(20, 8),
    confidence NUMERIC(3, 2),
    metadata JSONB,
    signal_generated BOOLEAN DEFAULT FALSE,
    scanned_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_scanner_results_scanner ON scanner_results (scanner_name, scanned_at DESC);
CREATE INDEX idx_scanner_results_symbol ON scanner_results (symbol, scanned_at DESC);

-- =====================================================
-- PORTFOLIO STATE (snapshot)
-- =====================================================

CREATE TABLE portfolio_snapshots (
    time TIMESTAMPTZ NOT NULL,
    total_value NUMERIC(20, 8) NOT NULL,
    available_balance NUMERIC(20, 8) NOT NULL,
    margin_used NUMERIC(20, 8),
    unrealized_pnl NUMERIC(20, 8),
    realized_pnl NUMERIC(20, 8),
    open_positions INTEGER,
    daily_return NUMERIC(10, 4),
    total_return NUMERIC(10, 4),
    sharpe_ratio NUMERIC(10, 4),
    max_drawdown NUMERIC(10, 4),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('portfolio_snapshots', 'time',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

-- =====================================================
-- SYSTEM METRICS (monitoring)
-- =====================================================

CREATE TABLE system_metrics (
    time TIMESTAMPTZ NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value NUMERIC(20, 4) NOT NULL,
    labels JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('system_metrics', 'time',
    chunk_time_interval => INTERVAL '1 hour',
    if_not_exists => TRUE
);

CREATE INDEX idx_system_metrics_name ON system_metrics (metric_name, time DESC);

-- =====================================================
-- AUDIT LOG (all important actions)
-- =====================================================

CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    event_type TEXT NOT NULL, -- 'order_placed', 'order_cancelled', 'risk_breach', etc.
    severity TEXT NOT NULL, -- 'info', 'warning', 'error', 'critical'
    component TEXT NOT NULL, -- 'executor', 'risk_manager', 'scanner', etc.
    message TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_log_type ON audit_log (event_type, created_at DESC);
CREATE INDEX idx_audit_log_severity ON audit_log (severity, created_at DESC);
CREATE INDEX idx_audit_log_component ON audit_log (component, created_at DESC);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Open positions with current P&L
CREATE VIEW open_positions_with_pnl AS
SELECT 
    p.*,
    (CASE 
        WHEN p.side = 'long' THEN (p.current_price - p.entry_price) * p.quantity
        ELSE (p.entry_price - p.current_price) * p.quantity
    END) as current_unrealized_pnl,
    (CASE 
        WHEN p.side = 'long' THEN ((p.current_price - p.entry_price) / p.entry_price) * 100
        ELSE ((p.entry_price - p.current_price) / p.entry_price) * 100
    END) as pnl_percent
FROM positions p
WHERE p.status = 'open';

-- Daily performance summary
CREATE VIEW daily_performance AS
SELECT
    DATE(executed_at) as trade_date,
    symbol,
    COUNT(*) as num_trades,
    SUM(CASE WHEN realized_pnl > 0 THEN 1 ELSE 0 END) as winning_trades,
    SUM(CASE WHEN realized_pnl <= 0 THEN 1 ELSE 0 END) as losing_trades,
    SUM(realized_pnl) as total_pnl,
    AVG(realized_pnl) as avg_pnl,
    MAX(realized_pnl) as max_win,
    MIN(realized_pnl) as max_loss
FROM executed_trades
WHERE realized_pnl IS NOT NULL
GROUP BY DATE(executed_at), symbol;

-- Recent scanner results (last 24h)
CREATE VIEW recent_scanner_results AS
SELECT 
    sr.*,
    s.id as signal_id,
    s.executed as signal_executed,
    o.status as order_status
FROM scanner_results sr
LEFT JOIN signals s ON sr.signal_generated = TRUE 
    AND s.symbol = sr.symbol 
    AND s.created_at >= sr.scanned_at - INTERVAL '5 minutes'
LEFT JOIN orders o ON s.order_id = o.id
WHERE sr.scanned_at >= NOW() - INTERVAL '24 hours'
ORDER BY sr.scanned_at DESC;
```

#### 2. **Database Migrations** (`infrastructure/database/migrations/`)

**Setup Alembic**:
```bash
# Install alembic
pip install alembic

# Initialize alembic
alembic init infrastructure/database/migrations

# Configure alembic.ini
```

**Migration template** (`infrastructure/database/migrations/env.py`):
```python
# infrastructure/database/migrations/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

# Load configuration
config = context.config

# Database URL from environment
database_url = os.getenv(
    'DATABASE_URL',
    'postgresql://trading:trading@localhost:5432/trading_system'
)
config.set_main_option('sqlalchemy.url', database_url)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Run migrations
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=None
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
```

**Initial migration** (`infrastructure/database/migrations/versions/001_initial_schema.py`):
```python
"""initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-15

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Read and execute schema.sql
    with open('infrastructure/database/schema.sql', 'r') as f:
        schema_sql = f.read()
    
    # Execute in parts (split by ;)
    for statement in schema_sql.split(';'):
        if statement.strip():
            op.execute(statement)

def downgrade():
    # Drop all tables
    op.execute('DROP SCHEMA public CASCADE')
    op.execute('CREATE SCHEMA public')
```

#### 3. **Database Client & Repository Pattern** (`infrastructure/database/`)

**a) TimescaleDB Client** (`infrastructure/database/timescale_client.py`):
```python
# infrastructure/database/timescale_client.py

import asyncpg
from typing import List, Dict, Optional, Any
from contextlib import asynccontextmanager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TimescaleDBClient:
    """
    Async PostgreSQL/TimescaleDB client with connection pooling.
    """
    
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        min_size: int = 10,
        max_size: int = 50
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.min_size = min_size
        self.max_size = max_size
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self):
        """Initialize connection pool."""
        self.pool = await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
            min_size=self.min_size,
            max_size=self.max_size,
            command_timeout=60
        )
        logger.info(f"Connected to TimescaleDB: {self.database}")
    
    async def disconnect(self):
        """Close connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Disconnected from TimescaleDB")
    
    @asynccontextmanager
    async def acquire(self):
        """Acquire connection from pool."""
        async with self.pool.acquire() as connection:
            yield connection
    
    async def execute(self, query: str, *args) -> str:
        """Execute a query without returning results."""
        async with self.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch(self, query: str, *args) -> List[asyncpg.Record]:
        """Fetch multiple rows."""
        async with self.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Fetch single row."""
        async with self.acquire() as conn:
            return await conn.fetchrow(query, *args)
    
    async def fetchval(self, query: str, *args) -> Any:
        """Fetch single value."""
        async with self.acquire() as conn:
            return await conn.fetchval(query, *args)
    
    async def executemany(self, query: str, args: List[tuple]) -> None:
        """Execute query with multiple parameter sets."""
        async with self.acquire() as conn:
            await conn.executemany(query, args)
    
    # ==========================================
    # CANDLES METHODS
    # ==========================================
    
    async def insert_candles(self, candles: List[Dict]):
        """
        Bulk insert candles.
        
        Args:
            candles: List of dicts with keys: time, symbol, exchange, 
                     timeframe, open, high, low, close, volume
        """
        query = """
            INSERT INTO candles 
            (time, symbol, exchange, timeframe, open, high, low, close, volume, 
             quote_volume, trades_count)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            ON CONFLICT DO NOTHING
        """
        
        values = [
            (
                c['time'],
                c['symbol'],
                c['exchange'],
                c['timeframe'],
                c['open'],
                c['high'],
                c['low'],
                c['close'],
                c['volume'],
                c.get('quote_volume'),
                c.get('trades_count')
            )
            for c in candles
        ]
        
        await self.executemany(query, values)
        logger.debug(f"Inserted {len(candles)} candles")
    
    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        start_time: datetime,
        end_time: datetime,
        exchange: str = 'binance'
    ) -> List[Dict]:
        """
        Retrieve candles for a time range.
        """
        query = """
            SELECT time, open, high, low, close, volume, quote_volume, trades_count
            FROM candles
            WHERE symbol = $1
                AND exchange = $2
                AND timeframe = $3
                AND time >= $4
                AND time <= $5
            ORDER BY time ASC
        """
        
        rows = await self.fetch(query, symbol, exchange, timeframe, start_time, end_time)
        
        return [
            {
                'time': row['time'],
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': float(row['volume']),
                'quote_volume': float(row['quote_volume']) if row['quote_volume'] else None,
                'trades_count': row['trades_count']
            }
            for row in rows
        ]
    
    async def get_latest_candle(
        self,
        symbol: str,
        timeframe: str,
        exchange: str = 'binance'
    ) -> Optional[Dict]:
        """Get most recent candle."""
        query = """
            SELECT time, open, high, low, close, volume
            FROM candles
            WHERE symbol = $1 AND exchange = $2 AND timeframe = $3
            ORDER BY time DESC
            LIMIT 1
        """
        
        row = await self.fetchrow(query, symbol, exchange, timeframe)
        
        if row:
            return {
                'time': row['time'],
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': float(row['volume'])
            }
        return None
    
    # ==========================================
    # ORDERS METHODS
    # ==========================================
    
    async def insert_order(self, order: Dict) -> str:
        """Insert order and return ID."""
        query = """
            INSERT INTO orders 
            (id, client_order_id, symbol, exchange, side, order_type, status,
             price, quantity, stop_loss, take_profit, time_in_force, reduce_only)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            RETURNING id
        """
        
        order_id = await self.fetchval(
            query,
            order['id'],
            order.get('client_order_id'),
            order['symbol'],
            order['exchange'],
            order['side'],
            order['order_type'],
            order['status'],
            order.get('price'),
            order['quantity'],
            order.get('stop_loss'),
            order.get('take_profit'),
            order.get('time_in_force', 'GTC'),
            order.get('reduce_only', False)
        )
        
        return order_id
    
    async def update_order_status(
        self,
        order_id: str,
        status: str,
        filled_quantity: Optional[float] = None,
        average_fill_price: Optional[float] = None
    ):
        """Update order status."""
        query = """
            UPDATE orders
            SET status = $2,
                filled_quantity = COALESCE($3, filled_quantity),
                average_fill_price = COALESCE($4, average_fill_price),
                updated_at = NOW(),
                filled_at = CASE WHEN $2 = 'filled' THEN NOW() ELSE filled_at END,
                cancelled_at = CASE WHEN $2 = 'cancelled' THEN NOW() ELSE cancelled_at END
            WHERE id = $1
        """
        
        await self.execute(query, order_id, status, filled_quantity, average_fill_price)
    
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get all open orders, optionally filtered by symbol."""
        if symbol:
            query = """
                SELECT * FROM orders
                WHERE status IN ('pending', 'partially_filled')
                    AND symbol = $1
                ORDER BY created_at DESC
            """
            rows = await self.fetch(query, symbol)
        else:
            query = """
                SELECT * FROM orders
                WHERE status IN ('pending', 'partially_filled')
                ORDER BY created_at DESC
            """
            rows = await self.fetch(query)
        
        return [dict(row) for row in rows]
    
    # ==========================================
    # POSITIONS METHODS
    # ==========================================
    
    async def insert_position(self, position: Dict) -> int:
        """Insert new position."""
        query = """
            INSERT INTO positions
            (symbol, exchange, side, quantity, entry_price, current_price,
             stop_loss, take_profit, opened_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id
        """
        
        position_id = await self.fetchval(
            query,
            position['symbol'],
            position['exchange'],
            position['side'],
            position['quantity'],
            position['entry_price'],
            position['current_price'],
            position.get('stop_loss'),
            position.get('take_profit'),
            position['opened_at']
        )
        
        return position_id
    
    async def get_open_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get all open positions."""
        if symbol:
            query = """
                SELECT * FROM open_positions_with_pnl
                WHERE symbol = $1
            """
            rows = await self.fetch(query, symbol)
        else:
            query = "SELECT * FROM open_positions_with_pnl"
            rows = await self.fetch(query)
        
        return [dict(row) for row in rows]
    
    async def update_position_price(self, position_id: int, current_price: float):
        """Update position current price and unrealized P&L."""
        query = """
            UPDATE positions
            SET current_price = $2,
                updated_at = NOW()
            WHERE id = $1
        """
        await self.execute(query, position_id, current_price)
    
    async def close_position(
        self,
        position_id: int,
        close_price: float,
        realized_pnl: float
    ):
        """Close a position."""
        query = """
            UPDATE positions
            SET status = 'closed',
                current_price = $2,
                realized_pnl = $3,
                closed_at = NOW(),
                updated_at = NOW()
            WHERE id = $1
        """
        await self.execute(query, position_id, close_price, realized_pnl)
    
    # ==========================================
    # SIGNALS METHODS
    # ==========================================
    
    async def insert_signal(self, signal: Dict) -> int:
        """Insert trading signal."""
        query = """
            INSERT INTO signals
            (strategy_name, symbol, exchange, signal_type, side, price,
             confidence, stop_loss, take_profit, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING id
        """
        
        signal_id = await self.fetchval(
            query,
            signal['strategy_name'],
            signal['symbol'],
            signal['exchange'],
            signal['signal_type'],
            signal['side'],
            signal['price'],
            signal.get('confidence'),
            signal.get('stop_loss'),
            signal.get('take_profit'),
            signal.get('metadata')
        )
        
        return signal_id
    
    async def mark_signal_executed(self, signal_id: int, order_id: str):
        """Mark signal as executed."""
        query = """
            UPDATE signals
            SET executed = TRUE,
                order_id = $2
            WHERE id = $1
        """
        await self.execute(query, signal_id, order_id)
    
    # ==========================================
    # LIQUIDATIONS METHODS (NEW)
    # ==========================================
    
    async def insert_liquidation(self, liquidation: Dict):
        """Insert liquidation event."""
        query = """
            INSERT INTO liquidations
            (time, symbol, exchange, side, price, quantity, quantity_usd)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
        """
        
        await self.execute(
            query,
            liquidation['time'],
            liquidation['symbol'],
            liquidation['exchange'],
            liquidation['side'],
            liquidation['price'],
            liquidation['quantity'],
            liquidation['quantity_usd']
        )
    
    async def get_recent_liquidations(
        self,
        symbol: str,
        minutes: int = 60,
        min_size_usd: float = 100000
    ) -> List[Dict]:
        """Get recent large liquidations."""
        query = """
            SELECT * FROM liquidations
            WHERE symbol = $1
                AND time >= NOW() - INTERVAL '1 minute' * $2
                AND quantity_usd >= $3
            ORDER BY time DESC
        """
        
        rows = await self.fetch(query, symbol, minutes, min_size_usd)
        return [dict(row) for row in rows]
    
    async def get_liquidation_zones(
        self,
        symbol: str,
        hours: int = 24
    ) -> List[Dict]:
        """Get aggregated liquidation zones."""
        query = """
            SELECT 
                price_level,
                side,
                SUM(total_usd) as total_usd,
                SUM(count) as liquidation_count
            FROM liquidations_by_level
            WHERE symbol = $1
                AND time >= NOW() - INTERVAL '1 hour' * $2
            GROUP BY price_level, side
            HAVING SUM(total_usd) > 1000000
            ORDER BY SUM(total_usd) DESC
        """
        
        rows = await self.fetch(query, symbol, hours)
        return [dict(row) for row in rows]
    
    # ==========================================
    # SCANNER RESULTS METHODS
    # ==========================================
    
    async def insert_scanner_result(self, result: Dict) -> int:
        """Insert scanner result."""
        query = """
            INSERT INTO scanner_results
            (scanner_name, symbol, exchange, entry_price, stop_loss,
             take_profit, confidence, metadata, scanned_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id
        """
        
        result_id = await self.fetchval(
            query,
            result['scanner_name'],
            result['symbol'],
            result['exchange'],
            result['entry_price'],
            result.get('stop_loss'),
            result.get('take_profit'),
            result.get('confidence'),
            result.get('metadata'),
            result['scanned_at']
        )
        
        return result_id
    
    # ==========================================
    # AUDIT LOG METHODS
    # ==========================================
    
    async def log_event(
        self,
        event_type: str,
        severity: str,
        component: str,
        message: str,
        metadata: Optional[Dict] = None
    ):
        """Log an audit event."""
        query = """
            INSERT INTO audit_log
            (event_type, severity, component, message, metadata)
            VALUES ($1, $2, $3, $4, $5)
        """
        
        await self.execute(query, event_type, severity, component, message, metadata)
```

**b) Redis Client** (`infrastructure/database/redis_client.py`):
```python
# infrastructure/database/redis_client.py

import redis.asyncio as aioredis
import json
from typing import Optional, Any, List
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    """
    Async Redis client for caching and pub/sub.
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        max_connections: int = 50
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.max_connections = max_connections
        self.redis: Optional[aioredis.Redis] = None
    
    async def connect(self):
        """Connect to Redis."""
        self.redis = await aioredis.from_url(
            f"redis://{self.host}:{self.port}/{self.db}",
            password=self.password,
            encoding="utf-8",
            decode_responses=True,
            max_connections=self.max_connections
        )
        logger.info(f"Connected to Redis: {self.host}:{self.port}")
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()
            logger.info("Disconnected from Redis")
    
    # ==========================================
    # BASIC OPERATIONS
    # ==========================================
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        return await self.redis.get(key)
    
    async def set(
        self,
        key: str,
        value: Any,
        ex: Optional[int] = None
    ) -> bool:
        """
        Set key-value pair.
        
        Args:
            key: Key name
            value: Value (will be JSON serialized if not string)
            ex: Expiration in seconds
        """
        if not isinstance(value, str):
            value = json.dumps(value)
        
        return await self.redis.set(key, value, ex=ex)
    
    async def delete(self, *keys: str) -> int:
        """Delete one or more keys."""
        return await self.redis.delete(*keys)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return await self.redis.exists(key) > 0
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration on key."""
        return await self.redis.expire(key, seconds)
    
    # ==========================================
    # HASH OPERATIONS
    # ==========================================
    
    async def hset(self, name: str, key: str, value: Any) -> int:
        """Set hash field."""
        if not isinstance(value, str):
            value = json.dumps(value)
        return await self.redis.hset(name, key, value)
    
    async def hget(self, name: str, key: str) -> Optional[str]:
        """Get hash field."""
        return await self.redis.hget(name, key)
    
    async def hgetall(self, name: str) -> dict:
        """Get all hash fields."""
        return await self.redis.hgetall(name)
    
    async def hdel(self, name: str, *keys: str) -> int:
        """Delete hash fields."""
        return await self.redis.hdel(name, *keys)
    
    # ==========================================
    # LIST OPERATIONS
    # ==========================================
    
    async def lpush(self, key: str, *values: Any) -> int:
        """Push to list (left)."""
        return await self.redis.lpush(key, *values)
    
    async def rpush(self, key: str, *values: Any) -> int:
        """Push to list (right)."""
        return await self.redis.rpush(key, *values)
    
    async def lpop(self, key: str) -> Optional[str]:
        """Pop from list (left)."""
        return await self.redis.lpop(key)
    
    async def rpop(self, key: str) -> Optional[str]:
        """Pop from list (right)."""
        return await self.redis.rpop(key)
    
    async def lrange(self, key: str, start: int, end: int) -> List[str]:
        """Get list range."""
        return await self.redis.lrange(key, start, end)
    
    # ==========================================
    # SORTED SET OPERATIONS
    # ==========================================
    
    async def zadd(self, key: str, mapping: dict) -> int:
        """Add to sorted set."""
        return await self.redis.zadd(key, mapping)
    
    async def zrange(
        self,
        key: str,
        start: int,
        end: int,
        withscores: bool = False
    ) -> List:
        """Get sorted set range."""
        return await self.redis.zrange(key, start, end, withscores=withscores)
    
    # ==========================================
    # CACHE HELPERS
    # ==========================================
    
    async def cache_candle(
        self,
        symbol: str,
        timeframe: str,
        candle: dict,
        ttl: int = 60
    ):
        """
        Cache latest candle.
        
        Key format: candle:{symbol}:{timeframe}
        TTL: 60 seconds default
        """
        key = f"candle:{symbol}:{timeframe}"
        await self.set(key, candle, ex=ttl)
    
    async def get_cached_candle(
        self,
        symbol: str,
        timeframe: str
    ) -> Optional[dict]:
        """Get cached candle."""
        key = f"candle:{symbol}:{timeframe}"
        data = await self.get(key)
        return json.loads(data) if data else None
    
    async def cache_orderbook(
        self,
        symbol: str,
        orderbook: dict,
        ttl: int = 5
    ):
        """
        Cache orderbook snapshot.
        
        TTL: 5 seconds (orderbook changes frequently)
        """
        key = f"orderbook:{symbol}"
        await self.set(key, orderbook, ex=ttl)
    
    async def get_cached_orderbook(self, symbol: str) -> Optional[dict]:
        """Get cached orderbook."""
        key = f"orderbook:{symbol}"
        data = await self.get(key)
        return json.loads(data) if data else None
    
    async def cache_position(
        self,
        symbol: str,
        position: dict
    ):
        """
        Cache open position.
        
        No TTL - cleared on position close.
        """
        key = f"position:{symbol}"
        await self.set(key, position)
    
    async def get_cached_position(self, symbol: str) -> Optional[dict]:
        """Get cached position."""
        key = f"position:{symbol}"
        data = await self.get(key)
        return json.loads(data) if data else None
    
    async def clear_position_cache(self, symbol: str):
        """Clear position cache."""
        key = f"position:{symbol}"
        await self.delete(key)
```

### **Criterios de Aceptación**:
- ✅ TimescaleDB schema deployed successfully
- ✅ All tables created with hypertables
- ✅ Compression policies active
- ✅ Continuous aggregates working
- ✅ Database client can insert 10k+ rows/s
- ✅ Redis caching working with <1ms latency
- ✅ Connection pooling handles 50+ concurrent connections
- ✅ Migrations run successfully forward/backward

### **Entregables**:
- Complete database schema
- Migration scripts
- TimescaleDB client
- Redis client
- Repository implementations
- 30+ database integration tests
- Performance benchmarks (insert/query speeds)

---

## **Sprint 2.2: Message Bus & Event System**
**Duración**: 2-3 días

### Tareas:

#### 1. **Redis Streams Implementation** (`infrastructure/message_bus/redis_streams.py`)

```python
# infrastructure/message_bus/redis_streams.py

import asyncio
import json
from typing import Dict, List, Callable, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RedisStreamsClient:
    """
    Redis Streams for event-driven architecture.
    
    Features:
    - Multiple streams for different event types
    - Consumer groups for parallel processing
    - Automatic acknowledgment
    - Dead letter queue for failed events
    """
    
    def __init__(self, redis_client):
        self.redis = redis_client.redis
        self.consumers = {}  # stream_name -> consumer task
        self.running = False
    
    # ==========================================
    # PUBLISHER
    # ==========================================
    
    async def publish(
        self,
        stream: str,
        data: Dict,
        max_len: int = 10000
    ) -> str:
        """
        Publish event to stream.
        
        Args:
            stream: Stream name (e.g., 'market_data:candles')
            data: Event data (will be JSON serialized)
            max_len: Max stream length (trimmed automatically)
        
        Returns:
            Message ID
        """
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.utcnow().isoformat()
        
        # Serialize data
        serialized = {k: json.dumps(v) for k, v in data.items()}
        
        # Add to stream with max length
        message_id = await self.redis.xadd(
            stream,
            serialized,
            maxlen=max_len
        )
        
        logger.debug(f"Published to {stream}: {message_id}")
        return message_id
    
    # ==========================================
    # CONSUMER
    # ==========================================
    
    async def consume(
        self,
        stream: str,
        group: str,
        consumer_name: str,
        callback: Callable,
        block_ms: int = 5000,
        count: int = 10
    ):
        """
        Consume events from stream.
        
        Args:
            stream: Stream name
            group: Consumer group name
            consumer_name: Unique consumer name
            callback: Async function(event_data) to process events
            block_ms: Block time in milliseconds
            count: Max messages per read
        """
        # Create consumer group if doesn't exist
        try:
            await self.redis.xgroup_create(
                stream,
                group,
                id='0',
                mkstream=True
            )
            logger.info(f"Created consumer group: {group} on {stream}")
        except Exception as e:
            # Group already exists
            pass
        
        logger.info(f"Starting consumer: {consumer_name} on {stream}")
        
        while self.running:
            try:
                # Read from stream
                messages = await self.redis.xreadgroup(
                    group,
                    consumer_name,
                    {stream: '>'},
                    count=count,
                    block=block_ms
                )
                
                if not messages:
                    continue
                
                # Process messages
                for stream_name, stream_messages in messages:
                    for message_id, data in stream_messages:
                        try:
                            # Deserialize
                            deserialized = {
                                k: json.loads(v) for k, v in data.items()
                            }
                            
                            # Call callback
                            await callback(deserialized)
                            
                            # Acknowledge
                            await self.redis.xack(stream, group, message_id)
                            
                        except Exception as e:
                            logger.error(
                                f"Error processing message {message_id}: {e}"
                            )
                            # Move to dead letter queue
                            await self._move_to_dlq(
                                stream,
                                message_id,
                                data,
                                str(e)
                            )
                            # Still acknowledge to remove from pending
                            await self.redis.xack(stream, group, message_id)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Consumer error: {e}")
                await asyncio.sleep(1)
        
        logger.info(f"Consumer stopped: {consumer_name}")
    
    async def start_consumer(
        self,
        stream: str,
        group: str,
        consumer_name: str,
        callback: Callable
    ):
        """Start consumer in background task."""
        self.running = True
        
        task = asyncio.create_task(
            self.consume(stream, group, consumer_name, callback)
        )
        
        self.consumers[f"{stream}:{consumer_name}"] = task
        return task
    
    async def stop_consumers(self):
        """Stop all consumers gracefully."""
        self.running = False
        
        # Wait for all consumers to finish
        for task in self.consumers.values():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        self.consumers.clear()
        logger.info("All consumers stopped")
    
    # ==========================================
    # DEAD LETTER QUEUE
    # ==========================================
    
    async def _move_to_dlq(
        self,
        stream: str,
        message_id: str,
        data: Dict,
        error: str
    ):
        """Move failed message to dead letter queue."""
        dlq_stream = f"{stream}:dlq"
        
        dlq_data = {
            'original_stream': stream,
            'original_message_id': message_id,
            'error': error,
            'failed_at': datetime.utcnow().isoformat(),
            'data': json.dumps(data)
        }
        
        await self.publish(dlq_stream, dlq_data, max_len=1000)
        logger.warning(f"Moved message to DLQ: {message_id}")
    
    # ==========================================
    # STREAM NAMES (conventions)
    # ==========================================
    
    CANDLES = "market_data:candles"
    TRADES = "market_data:trades"
    ORDERBOOK = "market_data:orderbook"
    LIQUIDATIONS = "market_data:liquidations"
    
    SIGNALS = "signals:generated"
    ORDERS = "orders:events"
    EXECUTIONS = "executions:events"
    POSITIONS = "positions:events"
    
    SCANNER_RESULTS = "scanner:results"
    RISK_ALERTS = "risk:alerts"
    SYSTEM_EVENTS = "system:events"
```

#### 2. **Event Bus Pattern** (`infrastructure/message_bus/event_bus.py`)

```python
# infrastructure/message_bus/event_bus.py

from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)

@dataclass
class Event:
    """Base event class."""
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str

class EventBus:
    """
    In-memory event bus for local event distribution.
    
    For distributed: Use Redis Streams.
    For local: Use this EventBus.
    """
    
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
        self.event_history: List[Event] = []
        self.max_history = 1000
    
    def subscribe(self, event_type: str, handler: Callable):
        """
        Subscribe to event type.
        
        Args:
            event_type: Event type string (e.g., 'order.filled')
            handler: Async function(event) to call
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        
        self.handlers[event_type].append(handler)
        logger.info(f"Subscribed to {event_type}: {handler.__name__}")
    
    def unsubscribe(self, event_type: str, handler: Callable):
        """Unsubscribe from event type."""
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)
    
    async def publish(self, event: Event):
        """
        Publish event to all subscribers.
        
        Args:
            event: Event object
        """
        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
        
        # Get handlers
        handlers = self.handlers.get(event.event_type, [])
        
        if not handlers:
            logger.debug(f"No handlers for {event.event_type}")
            return
        
        # Call all handlers
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(
                    f"Error in handler {handler.__name__} "
                    f"for {event.event_type}: {e}"
                )
    
    async def publish_and_wait(self, event: Event):
        """Publish event and wait for all handlers to complete."""
        handlers = self.handlers.get(event.event_type, [])
        
        if not handlers:
            return
        
        tasks = [handler(event) for handler in handlers]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_history(self, event_type: Optional[str] = None) -> List[Event]:
        """Get event history, optionally filtered by type."""
        if event_type:
            return [e for e in self.event_history if e.event_type == event_type]
        return self.event_history.copy()
```

#### 3. **Domain Events Integration** (`domain/events/`)

```python
# domain/events/order_events.py

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class OrderCreated:
    order_id: str
    symbol: str
    side: str
    order_type: str
    price: Optional[Decimal]
    quantity: Decimal
    stop_loss: Optional[Decimal]
    take_profit: Optional[Decimal]
    timestamp: datetime

@dataclass
class OrderFilled:
    order_id: str
    symbol: str
    side: str
    filled_price: Decimal
    filled_quantity: Decimal
    commission: Decimal
    timestamp: datetime

@dataclass
class OrderPartiallyFilled:
    order_id: str
    symbol: str
    filled_quantity: Decimal
    remaining_quantity: Decimal
    average_price: Decimal
    timestamp: datetime

@dataclass
class OrderCancelled:
    order_id: str
    symbol: str
    reason: str
    timestamp: datetime

@dataclass
class OrderRejected:
    order_id: str
    symbol: str
    reason: str
    timestamp: datetime


# domain/events/trade_events.py

@dataclass
class TradeExecuted:
    trade_id: str
    order_id: str
    symbol: str
    side: str
    price: Decimal
    quantity: Decimal
    commission: Decimal
    realized_pnl: Optional[Decimal]
    timestamp: datetime

@dataclass
class PositionOpened:
    position_id: int
    symbol: str
    side: str
    quantity: Decimal
    entry_price: Decimal
    stop_loss: Optional[Decimal]
    take_profit: Optional[Decimal]
    timestamp: datetime

@dataclass
class PositionClosed:
    position_id: int
    symbol: str
    side: str
    quantity: Decimal
    entry_price: Decimal
    exit_price: Decimal
    realized_pnl: Decimal
    duration_seconds: int
    timestamp: datetime

@dataclass
class PositionUpdated:
    position_id: int
    symbol: str
    current_price: Decimal
    unrealized_pnl: Decimal
    timestamp: datetime


# domain/events/market_events.py

@dataclass
class CandleClosed:
    symbol: str
    timeframe: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    timestamp: datetime

@dataclass
class PriceUpdated:
    symbol: str
    price: Decimal
    timestamp: datetime

@dataclass
class OrderBookUpdated:
    symbol: str
    best_bid: Decimal
    best_ask: Decimal
    bid_volume: Decimal
    ask_volume: Decimal
    timestamp: datetime

@dataclass
class LiquidationDetected:
    symbol: str
    side: str  # 'long' or 'short'
    price: Decimal
    quantity_usd: Decimal
    timestamp: datetime


# domain/events/signal_events.py

@dataclass
class SignalGenerated:
    strategy_name: str
    symbol: str
    signal_type: str  # 'entry', 'exit'
    side: str
    price: Decimal
    confidence: float
    stop_loss: Optional[Decimal]
    take_profit: Optional[Decimal]
    metadata: dict
    timestamp: datetime


# domain/events/risk_events.py

@dataclass
class RiskLimitBreached:
    limit_type: str  # 'position_size', 'daily_loss', etc.
    current_value: Decimal
    limit_value: Decimal
    severity: str  # 'warning', 'critical'
    timestamp: datetime

@dataclass
class CircuitBreakerTriggered:
    breaker_type: str  # 'daily_loss', 'volatility', etc.
    reason: str
    timestamp: datetime

@dataclass
class StopLossTriggered:
    position_id: int
    symbol: str
    stop_loss_price: Decimal
    current_price: Decimal
    timestamp: datetime
```

#### 4. **Event Publisher Service** (`infrastructure/message_bus/publisher.py`)

```python
# infrastructure/message_bus/publisher.py

from typing import Any
import logging

logger = logging.getLogger(__name__)

class EventPublisher:
    """
    Publish domain events to both local event bus and Redis Streams.
    """
    
    def __init__(
        self,
        event_bus: EventBus,
        redis_streams: RedisStreamsClient
    ):
        self.event_bus = event_bus
        self.redis_streams = redis_streams
    
    async def publish_order_created(self, event: OrderCreated):
        """Publish OrderCreated event."""
        # Local
        await self.event_bus.publish(Event(
            event_type='order.created',
            data=event.__dict__,
            timestamp=event.timestamp,
            source='executor'
        ))
        
        # Distributed
        await self.redis_streams.publish(
            RedisStreamsClient.ORDERS,
            {
                'event_type': 'order.created',
                'data': event.__dict__
            }
        )
    
    async def publish_order_filled(self, event: OrderFilled):
        """Publish OrderFilled event."""
        await self.event_bus.publish(Event(
            event_type='order.filled',
            data=event.__dict__,
            timestamp=event.timestamp,
            source='executor'
        ))
        
        await self.redis_streams.publish(
            RedisStreamsClient.ORDERS,
            {
                'event_type': 'order.filled',
                'data': event.__dict__
            }
        )
    
    async def publish_signal_generated(self, event: SignalGenerated):
        """Publish SignalGenerated event."""
        await self.event_bus.publish(Event(
            event_type='signal.generated',
            data=event.__dict__,
            timestamp=event.timestamp,
            source='strategy'
        ))
        
        await self.redis_streams.publish(
            RedisStreamsClient.SIGNALS,
            {
                'event_type': 'signal.generated',
                'data': event.__dict__
            }
        )
    
    async def publish_candle_closed(self, event: CandleClosed):
        """Publish CandleClosed event."""
        await self.redis_streams.publish(
            RedisStreamsClient.CANDLES,
            {
                'event_type': 'candle.closed',
                'data': event.__dict__
            }
        )
    
    async def publish_liquidation_detected(self, event: LiquidationDetected):
        """Publish LiquidationDetected event."""
        await self.redis_streams.publish(
            RedisStreamsClient.LIQUIDATIONS,
            {
                'event_type': 'liquidation.detected',
                'data': event.__dict__
            }
        )
    
    # Add more publish methods for all event types...
```

### **Criterios de Aceptación**:
- ✅ Redis Streams handles 1000+ events/s
- ✅ Consumer groups work correctly
- ✅ Failed events go to DLQ
- ✅ Event bus publishes to all subscribers
- ✅ <5ms p99 latency for publish
- ✅ No message loss
- ✅ Consumer can restart and continue from last position
- ✅ All domain events integrated

### **Entregables**:
- Redis Streams client
- Event bus implementation
- All domain events defined
- Event publisher service
- Consumer examples
- 20+ integration tests
- Performance benchmarks

---

**Tiempo total Sprint 2.1-2.2**: 5-7 días

## **Sprint 2.3: Exchange Connectors**
**Duración**: 3-4 días

### Tareas:

#### 1. **Base Exchange Interface** (`infrastructure/exchanges/base_exchange.py`)

```python
# infrastructure/exchanges/base_exchange.py

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Callable
from decimal import Decimal
from datetime import datetime
import asyncio

class BaseExchange(ABC):
    """
    Abstract base class for exchange adapters.
    
    All exchanges must implement this interface.
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.exchange_id = self.__class__.__name__.lower().replace('adapter', '')
        self.ws_connections = {}
        self.rate_limiter = None
    
    # ==========================================
    # AUTHENTICATION & CONNECTION
    # ==========================================
    
    @abstractmethod
    async def connect(self):
        """Initialize connection to exchange."""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """Close connections to exchange."""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Test if connection is working."""
        pass
    
    # ==========================================
    # MARKET DATA
    # ==========================================
    
    @abstractmethod
    async def get_ticker(self, symbol: str) -> Dict:
        """
        Get current ticker.
        
        Returns:
            {
                'symbol': 'BTC/USDT',
                'bid': Decimal('50000.0'),
                'ask': Decimal('50001.0'),
                'last': Decimal('50000.5'),
                'volume': Decimal('1000.0')
            }
        """
        pass
    
    @abstractmethod
    async def get_orderbook(self, symbol: str, limit: int = 20) -> Dict:
        """
        Get orderbook snapshot.
        
        Returns:
            {
                'symbol': 'BTC/USDT',
                'bids': [[price, quantity], ...],
                'asks': [[price, quantity], ...],
                'timestamp': datetime
            }
        """
        pass
    
    @abstractmethod
    async def get_recent_trades(self, symbol: str, limit: int = 100) -> List[Dict]:
        """Get recent trades."""
        pass
    
    @abstractmethod
    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        since: Optional[datetime] = None,
        limit: int = 500
    ) -> List[Dict]:
        """
        Get historical candles.
        
        Returns:
            [
                {
                    'timestamp': datetime,
                    'open': Decimal,
                    'high': Decimal,
                    'low': Decimal,
                    'close': Decimal,
                    'volume': Decimal
                },
                ...
            ]
        """
        pass
    
    # ==========================================
    # ACCOUNT
    # ==========================================
    
    @abstractmethod
    async def get_balance(self) -> Dict[str, Decimal]:
        """
        Get account balance.
        
        Returns:
            {
                'USDT': {'free': Decimal('10000'), 'locked': Decimal('100')},
                'BTC': {'free': Decimal('1.5'), 'locked': Decimal('0')}
            }
        """
        pass
    
    @abstractmethod
    async def get_positions(self) -> List[Dict]:
        """
        Get open positions.
        
        Returns:
            [
                {
                    'symbol': 'BTC/USDT',
                    'side': 'long',
                    'size': Decimal('0.1'),
                    'entry_price': Decimal('50000'),
                    'mark_price': Decimal('51000'),
                    'liquidation_price': Decimal('45000'),
                    'unrealized_pnl': Decimal('100')
                },
                ...
            ]
        """
        pass
    
    # ==========================================
    # ORDERS
    # ==========================================
    
    @abstractmethod
    async def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: Decimal,
        reduce_only: bool = False
    ) -> Dict:
        """
        Place market order.
        
        Returns:
            {
                'order_id': '12345',
                'symbol': 'BTC/USDT',
                'status': 'filled',
                'filled_price': Decimal('50000'),
                'filled_quantity': Decimal('0.1')
            }
        """
        pass
    
    @abstractmethod
    async def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: Decimal,
        price: Decimal,
        time_in_force: str = 'GTC',
        reduce_only: bool = False
    ) -> Dict:
        """Place limit order."""
        pass
    
    @abstractmethod
    async def place_stop_order(
        self,
        symbol: str,
        side: str,
        quantity: Decimal,
        stop_price: Decimal,
        order_type: str = 'STOP_MARKET'
    ) -> Dict:
        """Place stop loss order."""
        pass
    
    @abstractmethod
    async def cancel_order(self, symbol: str, order_id: str) -> bool:
        """Cancel order."""
        pass
    
    @abstractmethod
    async def cancel_all_orders(self, symbol: str) -> int:
        """
        Cancel all open orders for symbol.
        
        Returns:
            Number of orders cancelled
        """
        pass
    
    @abstractmethod
    async def get_order(self, symbol: str, order_id: str) -> Dict:
        """Get order details."""
        pass
    
    @abstractmethod
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get all open orders."""
        pass
    
    # ==========================================
    # MARKET INFO
    # ==========================================
    
    @abstractmethod
    async def get_market_info(self, symbol: str) -> Dict:
        """
        Get market information (precision, limits, etc).
        
        Returns:
            {
                'symbol': 'BTC/USDT',
                'price_precision': 2,
                'quantity_precision': 3,
                'min_quantity': Decimal('0.001'),
                'max_quantity': Decimal('1000'),
                'min_notional': Decimal('10')
            }
        """
        pass
    
    @abstractmethod
    async def get_trading_fees(self, symbol: str) -> Dict:
        """
        Get trading fees.
        
        Returns:
            {
                'maker': Decimal('0.0002'),
                'taker': Decimal('0.0004')
            }
        """
        pass
    
    @abstractmethod
    async def get_all_symbols(self) -> List[str]:
        """Get all tradeable symbols."""
        pass
    
    # ==========================================
    # WEBSOCKET SUBSCRIPTIONS
    # ==========================================
    
    @abstractmethod
    async def subscribe_trades(
        self,
        symbol: str,
        callback: Callable
    ):
        """
        Subscribe to trade stream.
        
        Callback receives:
            {
                'symbol': 'BTC/USDT',
                'price': Decimal('50000'),
                'quantity': Decimal('0.1'),
                'side': 'buy',
                'timestamp': datetime
            }
        """
        pass
    
    @abstractmethod
    async def subscribe_orderbook(
        self,
        symbol: str,
        callback: Callable
    ):
        """Subscribe to orderbook updates."""
        pass
    
    @abstractmethod
    async def subscribe_candles(
        self,
        symbol: str,
        timeframe: str,
        callback: Callable
    ):
        """Subscribe to candle/kline stream."""
        pass
    
    @abstractmethod
    async def subscribe_user_data(
        self,
        on_order_update: Optional[Callable] = None,
        on_balance_update: Optional[Callable] = None,
        on_position_update: Optional[Callable] = None
    ):
        """Subscribe to user data stream (orders, positions, balance)."""
        pass
    
    # ==========================================
    # HELPERS
    # ==========================================
    
    def normalize_symbol(self, symbol: str) -> str:
        """Normalize symbol to exchange format."""
        return symbol.replace('/', '')
    
    def denormalize_symbol(self, symbol: str) -> str:
        """Convert exchange symbol to standard format."""
        # Override in subclass if needed
        return symbol
    
    async def has_market(self, symbol: str) -> bool:
        """Check if exchange supports symbol."""
        symbols = await self.get_all_symbols()
        return symbol in symbols


#### 2. **Binance Adapter** (`infrastructure/exchanges/binance_adapter.py`)

```python
# infrastructure/exchanges/binance_adapter.py

import ccxt.async_support as ccxt
import websockets
import json
import hmac
import hashlib
from typing import List, Dict, Optional, Callable
from decimal import Decimal
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)

class BinanceAdapter(BaseExchange):
    """
    Binance exchange adapter.
    
    Supports:
    - Spot trading
    - Futures trading (USDT-M)
    - WebSocket streams
    """
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        testnet: bool = False,
        futures: bool = False
    ):
        super().__init__(api_key, api_secret, testnet)
        self.futures = futures
        
        # Initialize CCXT
        if futures:
            if testnet:
                self.ccxt = ccxt.binanceusdm({
                    'apiKey': api_key,
                    'secret': api_secret,
                    'options': {'defaultType': 'future'},
                    'urls': {
                        'api': {
                            'public': 'https://testnet.binancefuture.com/fapi/v1',
                            'private': 'https://testnet.binancefuture.com/fapi/v1'
                        }
                    }
                })
            else:
                self.ccxt = ccxt.binanceusdm({
                    'apiKey': api_key,
                    'secret': api_secret,
                    'options': {'defaultType': 'future'}
                })
        else:
            self.ccxt = ccxt.binance({
                'apiKey': api_key,
                'secret': api_secret,
                'enableRateLimit': True
            })
        
        # WebSocket URLs
        if futures:
            if testnet:
                self.ws_base_url = 'wss://stream.binancefuture.com'
            else:
                self.ws_base_url = 'wss://fstream.binance.com'
        else:
            self.ws_base_url = 'wss://stream.binance.com:9443'
    
    # ==========================================
    # CONNECTION
    # ==========================================
    
    async def connect(self):
        """Initialize connection."""
        await self.ccxt.load_markets()
        logger.info(f"Connected to Binance ({'Futures' if self.futures else 'Spot'})")
    
    async def disconnect(self):
        """Close connections."""
        await self.ccxt.close()
        
        # Close WebSocket connections
        for ws in self.ws_connections.values():
            await ws.close()
        
        logger.info("Disconnected from Binance")
    
    async def test_connection(self) -> bool:
        """Test connection."""
        try:
            await self.ccxt.fetch_time()
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    # ==========================================
    # MARKET DATA
    # ==========================================
    
    async def get_ticker(self, symbol: str) -> Dict:
        """Get ticker."""
        ticker = await self.ccxt.fetch_ticker(symbol)
        
        return {
            'symbol': symbol,
            'bid': Decimal(str(ticker['bid'])),
            'ask': Decimal(str(ticker['ask'])),
            'last': Decimal(str(ticker['last'])),
            'volume': Decimal(str(ticker['baseVolume']))
        }
    
    async def get_orderbook(self, symbol: str, limit: int = 20) -> Dict:
        """Get orderbook."""
        orderbook = await self.ccxt.fetch_order_book(symbol, limit)
        
        return {
            'symbol': symbol,
            'bids': [[Decimal(str(p)), Decimal(str(q))] for p, q in orderbook['bids']],
            'asks': [[Decimal(str(p)), Decimal(str(q))] for p, q in orderbook['asks']],
            'timestamp': datetime.fromtimestamp(orderbook['timestamp'] / 1000)
        }
    
    async def get_recent_trades(self, symbol: str, limit: int = 100) -> List[Dict]:
        """Get recent trades."""
        trades = await self.ccxt.fetch_trades(symbol, limit=limit)
        
        return [
            {
                'id': t['id'],
                'symbol': symbol,
                'price': Decimal(str(t['price'])),
                'quantity': Decimal(str(t['amount'])),
                'side': t['side'],
                'timestamp': datetime.fromtimestamp(t['timestamp'] / 1000)
            }
            for t in trades
        ]
    
    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        since: Optional[datetime] = None,
        limit: int = 500
    ) -> List[Dict]:
        """Get candles."""
        since_ms = int(since.timestamp() * 1000) if since else None
        
        candles = await self.ccxt.fetch_ohlcv(
            symbol,
            timeframe,
            since=since_ms,
            limit=limit
        )
        
        return [
            {
                'timestamp': datetime.fromtimestamp(c[0] / 1000),
                'open': Decimal(str(c[1])),
                'high': Decimal(str(c[2])),
                'low': Decimal(str(c[3])),
                'close': Decimal(str(c[4])),
                'volume': Decimal(str(c[5]))
            }
            for c in candles
        ]
    
    # ==========================================
    # ACCOUNT
    # ==========================================
    
    async def get_balance(self) -> Dict[str, Decimal]:
        """Get balance."""
        balance = await self.ccxt.fetch_balance()
        
        result = {}
        for currency, amounts in balance['total'].items():
            if amounts > 0:
                result[currency] = {
                    'free': Decimal(str(balance['free'].get(currency, 0))),
                    'locked': Decimal(str(balance['used'].get(currency, 0)))
                }
        
        return result
    
    async def get_positions(self) -> List[Dict]:
        """Get positions (futures only)."""
        if not self.futures:
            return []
        
        positions = await self.ccxt.fetch_positions()
        
        result = []
        for pos in positions:
            if float(pos.get('contracts', 0)) != 0:
                result.append({
                    'symbol': pos['symbol'],
                    'side': 'long' if float(pos['contracts']) > 0 else 'short',
                    'size': Decimal(str(abs(float(pos['contracts'])))),
                    'entry_price': Decimal(str(pos['entryPrice'])),
                    'mark_price': Decimal(str(pos['markPrice'])),
                    'liquidation_price': Decimal(str(pos.get('liquidationPrice', 0))),
                    'unrealized_pnl': Decimal(str(pos.get('unrealizedPnl', 0)))
                })
        
        return result
    
    # ==========================================
    # ORDERS
    # ==========================================
    
    async def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: Decimal,
        reduce_only: bool = False
    ) -> Dict:
        """Place market order."""
        params = {}
        if reduce_only and self.futures:
            params['reduceOnly'] = True
        
        order = await self.ccxt.create_market_order(
            symbol,
            side,
            float(quantity),
            params=params
        )
        
        return {
            'order_id': order['id'],
            'symbol': symbol,
            'status': order['status'],
            'filled_price': Decimal(str(order.get('average', 0))),
            'filled_quantity': Decimal(str(order.get('filled', 0)))
        }
    
    async def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: Decimal,
        price: Decimal,
        time_in_force: str = 'GTC',
        reduce_only: bool = False
    ) -> Dict:
        """Place limit order."""
        params = {'timeInForce': time_in_force}
        if reduce_only and self.futures:
            params['reduceOnly'] = True
        
        order = await self.ccxt.create_limit_order(
            symbol,
            side,
            float(quantity),
            float(price),
            params=params
        )
        
        return {
            'order_id': order['id'],
            'symbol': symbol,
            'status': order['status']
        }
    
    async def place_stop_order(
        self,
        symbol: str,
        side: str,
        quantity: Decimal,
        stop_price: Decimal,
        order_type: str = 'STOP_MARKET'
    ) -> Dict:
        """Place stop order."""
        params = {
            'stopPrice': float(stop_price),
            'type': order_type
        }
        
        order = await self.ccxt.create_order(
            symbol,
            order_type.lower(),
            side,
            float(quantity),
            params=params
        )
        
        return {
            'order_id': order['id'],
            'symbol': symbol,
            'status': order['status']
        }
    
    async def cancel_order(self, symbol: str, order_id: str) -> bool:
        """Cancel order."""
        try:
            await self.ccxt.cancel_order(order_id, symbol)
            return True
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {e}")
            return False
    
    async def cancel_all_orders(self, symbol: str) -> int:
        """Cancel all orders."""
        orders = await self.get_open_orders(symbol)
        count = 0
        
        for order in orders:
            if await self.cancel_order(symbol, order['id']):
                count += 1
        
        return count
    
    async def get_order(self, symbol: str, order_id: str) -> Dict:
        """Get order."""
        order = await self.ccxt.fetch_order(order_id, symbol)
        
        return {
            'id': order['id'],
            'symbol': symbol,
            'side': order['side'],
            'type': order['type'],
            'status': order['status'],
            'price': Decimal(str(order.get('price', 0))),
            'quantity': Decimal(str(order['amount'])),
            'filled': Decimal(str(order['filled'])),
            'remaining': Decimal(str(order['remaining']))
        }
    
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get open orders."""
        orders = await self.ccxt.fetch_open_orders(symbol)
        
        return [
            {
                'id': o['id'],
                'symbol': o['symbol'],
                'side': o['side'],
                'type': o['type'],
                'status': o['status'],
                'price': Decimal(str(o.get('price', 0))),
                'quantity': Decimal(str(o['amount'])),
                'filled': Decimal(str(o['filled']))
            }
            for o in orders
        ]
    
    # ==========================================
    # MARKET INFO
    # ==========================================
    
    async def get_market_info(self, symbol: str) -> Dict:
        """Get market info."""
        market = self.ccxt.market(symbol)
        
        return {
            'symbol': symbol,
            'price_precision': market['precision']['price'],
            'quantity_precision': market['precision']['amount'],
            'min_quantity': Decimal(str(market['limits']['amount']['min'])),
            'max_quantity': Decimal(str(market['limits']['amount']['max'])),
            'min_notional': Decimal(str(market['limits']['cost']['min']))
        }
    
    async def get_trading_fees(self, symbol: str) -> Dict:
        """Get fees."""
        fees = await self.ccxt.fetch_trading_fees()
        
        symbol_fees = fees.get(symbol, {'maker': 0.0002, 'taker': 0.0004})
        
        return {
            'maker': Decimal(str(symbol_fees['maker'])),
            'taker': Decimal(str(symbol_fees['taker']))
        }
    
    async def get_all_symbols(self) -> List[str]:
        """Get all symbols."""
        markets = await self.ccxt.load_markets()
        return list(markets.keys())
    
    # ==========================================
    # WEBSOCKET
    # ==========================================
    
    async def subscribe_trades(self, symbol: str, callback: Callable):
        """Subscribe to trades."""
        stream = f"{self.normalize_symbol(symbol).lower()}@trade"
        url = f"{self.ws_base_url}/ws/{stream}"
        
        async def handle_message():
            async with websockets.connect(url) as ws:
                self.ws_connections[f"trades_{symbol}"] = ws
                
                async for message in ws:
                    data = json.loads(message)
                    
                    await callback({
                        'symbol': symbol,
                        'price': Decimal(data['p']),
                        'quantity': Decimal(data['q']),
                        'side': 'buy' if data['m'] else 'sell',
                        'timestamp': datetime.fromtimestamp(data['T'] / 1000)
                    })
        
        asyncio.create_task(handle_message())
    
    async def subscribe_orderbook(self, symbol: str, callback: Callable):
        """Subscribe to orderbook."""
        stream = f"{self.normalize_symbol(symbol).lower()}@depth20@100ms"
        url = f"{self.ws_base_url}/ws/{stream}"
        
        async def handle_message():
            async with websockets.connect(url) as ws:
                self.ws_connections[f"orderbook_{symbol}"] = ws
                
                async for message in ws:
                    data = json.loads(message)
                    
                    await callback({
                        'symbol': symbol,
                        'bids': [[Decimal(p), Decimal(q)] for p, q in data['bids']],
                        'asks': [[Decimal(p), Decimal(q)] for p, q in data['asks']],
                        'timestamp': datetime.fromtimestamp(data['E'] / 1000)
                    })
        
        asyncio.create_task(handle_message())
    
    async def subscribe_candles(
        self,
        symbol: str,
        timeframe: str,
        callback: Callable
    ):
        """Subscribe to candles."""
        stream = f"{self.normalize_symbol(symbol).lower()}@kline_{timeframe}"
        url = f"{self.ws_base_url}/ws/{stream}"
        
        async def handle_message():
            async with websockets.connect(url) as ws:
                self.ws_connections[f"candles_{symbol}_{timeframe}"] = ws
                
                async for message in ws:
                    data = json.loads(message)
                    k = data['k']
                    
                    # Only emit closed candles
                    if k['x']:
                        await callback({
                            'symbol': symbol,
                            'timeframe': timeframe,
                            'timestamp': datetime.fromtimestamp(k['t'] / 1000),
                            'open': Decimal(k['o']),
                            'high': Decimal(k['h']),
                            'low': Decimal(k['l']),
                            'close': Decimal(k['c']),
                            'volume': Decimal(k['v'])
                        })
        
        asyncio.create_task(handle_message())
    
    async def subscribe_user_data(
        self,
        on_order_update: Optional[Callable] = None,
        on_balance_update: Optional[Callable] = None,
        on_position_update: Optional[Callable] = None
    ):
        """Subscribe to user data stream."""
        # Get listen key
        if self.futures:
            listen_key_response = await self.ccxt.fapiPrivatePostListenKey()
        else:
            listen_key_response = await self.ccxt.privatePostUserDataStream()
        
        listen_key = listen_key_response['listenKey']
        
        # WebSocket URL
        url = f"{self.ws_base_url}/ws/{listen_key}"
        
        async def handle_message():
            async with websockets.connect(url) as ws:
                self.ws_connections['user_data'] = ws
                
                # Keep-alive task (ping every 30 minutes)
                async def keep_alive():
                    while True:
                        await asyncio.sleep(1800)
                        if self.futures:
                            await self.ccxt.fapiPrivatePutListenKey({'listenKey': listen_key})
                        else:
                            await self.ccxt.privatePutUserDataStream({'listenKey': listen_key})
                
                asyncio.create_task(keep_alive())
                
                async for message in ws:
                    data = json.loads(message)
                    
                    event_type = data.get('e')
                    
                    if event_type == 'executionReport' and on_order_update:
                        # Order update
                        await on_order_update({
                            'order_id': data['i'],
                            'symbol': data['s'],
                            'status': self._map_order_status(data['X']),
                            'side': data['S'].lower(),
                            'filled_quantity': Decimal(data['z']),
                            'average_price': Decimal(data['Z']) / Decimal(data['z']) if float(data['z']) > 0 else Decimal(0)
                        })
                    
                    elif event_type == 'outboundAccountPosition' and on_balance_update:
                        # Balance update
                        balances = {
                            b['a']: {
                                'free': Decimal(b['f']),
                                'locked': Decimal(b['l'])
                            }
                            for b in data['B']
                        }
                        await on_balance_update(balances)
                    
                    elif event_type == 'ACCOUNT_UPDATE' and on_position_update:
                        # Position update (futures)
                        for pos in data['a']['P']:
                            await on_position_update({
                                'symbol': pos['s'],
                                'side': 'long' if float(pos['pa']) > 0 else 'short',
                                'size': Decimal(abs(float(pos['pa']))),
                                'entry_price': Decimal(pos['ep']),
                                'unrealized_pnl': Decimal(pos['up'])
                            })
        
        asyncio.create_task(handle_message())
    
    def _map_order_status(self, binance_status: str) -> str:
        """Map Binance order status to standard."""
        mapping = {
            'NEW': 'pending',
            'PARTIALLY_FILLED': 'partially_filled',
            'FILLED': 'filled',
            'CANCELED': 'cancelled',
            'REJECTED': 'rejected',
            'EXPIRED': 'expired'
        }
        return mapping.get(binance_status, 'unknown')


#### 3. **Rate Limiter** (`infrastructure/exchanges/rate_limiter.py`)

```python
# infrastructure/exchanges/rate_limiter.py

import asyncio
from datetime import datetime, timedelta
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class TokenBucketRateLimiter:
    """
    Token bucket rate limiter.
    
    Prevents exceeding exchange rate limits.
    """
    
    def __init__(
        self,
        max_tokens: int,
        refill_rate: float,  # tokens per second
        burst_size: Optional[int] = None
    ):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.burst_size = burst_size or max_tokens
        
        self.tokens = max_tokens
        self.last_refill = datetime.utcnow()
        self.lock = asyncio.Lock()
    
    async def acquire(self, tokens: int = 1):
        """
        Acquire tokens (wait if not available).
        """
        async with self.lock:
            while self.tokens < tokens:
                # Refill tokens
                now = datetime.utcnow()
                time_passed = (now - self.last_refill).total_seconds()
                new_tokens = time_passed * self.refill_rate
                
                self.tokens = min(
                    self.tokens + new_tokens,
                    self.burst_size
                )
                self.last_refill = now
                
                if self.tokens < tokens:
                    # Not enough tokens, wait
                    wait_time = (tokens - self.tokens) / self.refill_rate
                    await asyncio.sleep(wait_time)
            
            # Consume tokens
            self.tokens -= tokens
    
    async def try_acquire(self, tokens: int = 1) -> bool:
        """
        Try to acquire tokens (non-blocking).
        
        Returns:
            True if acquired, False otherwise
        """
        async with self.lock:
            # Refill tokens
            now = datetime.utcnow()
            time_passed = (now - self.last_refill).total_seconds()
            new_tokens = time_passed * self.refill_rate
            
            self.tokens = min(
                self.tokens + new_tokens,
                self.burst_size
            )
            self.last_refill = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            return False


class ExchangeRateLimiter:
    """
    Multi-endpoint rate limiter for exchanges.
    
    Different endpoints have different limits.
    """
    
    def __init__(self):
        self.limiters: Dict[str, TokenBucketRateLimiter] = {}
    
    def add_endpoint(
        self,
        endpoint: str,
        max_requests: int,
        window_seconds: int
    ):
        """
        Add endpoint with limit.
        
        Args:
            endpoint: Endpoint name (e.g., 'orders', 'market_data')
            max_requests: Max requests in window window_seconds: Time window in seconds
        """
        refill_rate = max_requests / window_seconds
        
        self.limiters[endpoint] = TokenBucketRateLimiter(
            max_tokens=max_requests,
            refill_rate=refill_rate,
            burst_size=max_requests
        )
    
    async def acquire(self, endpoint: str, tokens: int = 1):
        """Acquire tokens for endpoint."""
        if endpoint not in self.limiters:
            logger.warning(f"No rate limit configured for {endpoint}")
            return
        
        await self.limiters[endpoint].acquire(tokens)
    
    @classmethod
    def for_binance(cls) -> 'ExchangeRateLimiter':
        """
        Create rate limiter with Binance limits.
        
        Binance limits:
        - Orders: 300/min weight, 10/s orders
        - Market data: 2400/min weight
        """
        limiter = cls()
        
        # Order placement (10 per second)
        limiter.add_endpoint('place_order', max_requests=10, window_seconds=1)
        
        # Order cancellation (10 per second)
        limiter.add_endpoint('cancel_order', max_requests=10, window_seconds=1)
        
        # Market data (2400 per minute = 40 per second)
        limiter.add_endpoint('market_data', max_requests=40, window_seconds=1)
        
        # Account data (1200 per minute = 20 per second)
        limiter.add_endpoint('account', max_requests=20, window_seconds=1)
        
        return limiter


#### 4. **Exchange Factory** (`infrastructure/exchanges/exchange_factory.py`)

```python
# infrastructure/exchanges/exchange_factory.py

from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ExchangeFactory:
    """
    Factory for creating exchange adapters.
    """
    
    @staticmethod
    def create(
        exchange_id: str,
        api_key: str,
        api_secret: str,
        testnet: bool = False,
        **kwargs
    ) -> BaseExchange:
        """
        Create exchange adapter.
        
        Args:
            exchange_id: 'binance', 'hyperliquid', etc.
            api_key: API key
            api_secret: API secret
            testnet: Use testnet
            **kwargs: Exchange-specific options
        
        Returns:
            Exchange adapter instance
        """
        exchange_id = exchange_id.lower()
        
        if exchange_id == 'binance':
            from .binance_adapter import BinanceAdapter
            return BinanceAdapter(
                api_key,
                api_secret,
                testnet=testnet,
                futures=kwargs.get('futures', False)
            )
        
        elif exchange_id == 'hyperliquid':
            from .hyperliquid_adapter import HyperLiquidAdapter
            return HyperLiquidAdapter(api_key, api_secret, testnet=testnet)
        
        elif exchange_id == 'coinbase':
            from .coinbase_adapter import CoinbaseAdapter
            return CoinbaseAdapter(api_key, api_secret, testnet=testnet)
        
        else:
            raise ValueError(f"Unsupported exchange: {exchange_id}")
    
    @staticmethod
    def create_multiple(
        exchanges_config: Dict[str, Dict]
    ) -> Dict[str, BaseExchange]:
        """
        Create multiple exchange adapters.
        
        Args:
            exchanges_config: {
                'binance': {'api_key': '...', 'api_secret': '...', 'testnet': True},
                'hyperliquid': {...}
            }
        
        Returns:
            Dict of exchange_id -> adapter
        """
        adapters = {}
        
        for exchange_id, config in exchanges_config.items():
            try:
                adapter = ExchangeFactory.create(exchange_id, **config)
                adapters[exchange_id] = adapter
                logger.info(f"Created adapter for {exchange_id}")
            except Exception as e:
                logger.error(f"Failed to create adapter for {exchange_id}: {e}")
        
        return adapters


### **Criterios de Aceptación**:
- ✅ Base exchange interface completa
- ✅ Binance adapter funciona (testnet)
- ✅ WebSocket reconnect automático
- ✅ Rate limiting previene bans
- ✅ Order placement <50ms p99
- ✅ Market data streaming funciona
- ✅ User data stream funciona
- ✅ Factory pattern crea exchanges correctamente
- ✅ 25+ integration tests (testnet)

### **Entregables**:
- Base exchange interface
- Binance adapter completo
- Rate limiter
- Exchange factory
- WebSocket handlers
- 30+ tests
- Performance benchmarks

---

## 📡 FASE 3: MARKET DATA ENGINE (Semana 4)

## **Sprint 3.1: Market Data Pipeline**
**Duración**: 3-4 días

### Tareas:

#### 1. **Data Feed Manager** (`market_data/feeds/feed_manager.py`)

```python
# market_data/feeds/feed_manager.py

from typing import Dict, List, Callable, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class MarketDataFeedManager:
    """
    Manage multiple market data feeds.
    
    Responsibilities:
    - Subscribe to multiple exchanges
    - Normalize data
    - Distribute to consumers
    - Handle disconnections
    """
    
    def __init__(
        self,
        exchanges: Dict[str, BaseExchange],
        redis_streams: RedisStreamsClient,
        db_client: TimescaleDBClient
    ):
        self.exchanges = exchanges
        self.redis_streams = redis_streams
        self.db = db_client
        
        self.subscriptions = {}
        self.running = False
    
    async def start(self):
        """Start all feeds."""
        self.running = True
        logger.info("Starting market data feeds...")
        
        for exchange_id, exchange in self.exchanges.items():
            await exchange.connect()
        
        logger.info("Market data feeds started")
    
    async def stop(self):
        """Stop all feeds."""
        self.running = False
        logger.info("Stopping market data feeds...")
        
        for exchange in self.exchanges.values():
            await exchange.disconnect()
        
        logger.info("Market data feeds stopped")
    
    # ==========================================
    # CANDLES
    # ==========================================
    
    async def subscribe_candles(
        self,
        exchange_id: str,
        symbol: str,
        timeframe: str
    ):
        """
        Subscribe to candle stream.
        """
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            raise ValueError(f"Exchange {exchange_id} not found")
        
        async def on_candle(candle_data):
            # Normalize
            candle = {
                'time': candle_data['timestamp'],
                'symbol': symbol,
                'exchange': exchange_id,
                'timeframe': timeframe,
                'open': candle_data['open'],
                'high': candle_data['high'],
                'low': candle_data['low'],
                'close': candle_data['close'],
                'volume': candle_data['volume']
            }
            
            # Store in DB
            await self.db.insert_candles([candle])
            
            # Publish to streams
            await self.redis_streams.publish(
                RedisStreamsClient.CANDLES,
                {
                    'exchange': exchange_id,
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'data': candle
                }
            )
            
            logger.debug(f"Candle: {symbol} {timeframe} {candle['close']}")
        
        await exchange.subscribe_candles(symbol, timeframe, on_candle)
        
        sub_key = f"{exchange_id}:{symbol}:{timeframe}:candles"
        self.subscriptions[sub_key] = True
    
    # ==========================================
    # TRADES
    # ==========================================
    
    async def subscribe_trades(
        self,
        exchange_id: str,
        symbol: str
    ):
        """Subscribe to trade stream."""
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            raise ValueError(f"Exchange {exchange_id} not found")
        
        async def on_trade(trade_data):
            # Store in DB
            trade = {
                'time': trade_data['timestamp'],
                'trade_id': str(trade_data.get('id', '')),
                'symbol': symbol,
                'exchange': exchange_id,
                'price': trade_data['price'],
                'quantity': trade_data['quantity'],
                'side': trade_data['side']
            }
            
            # Batch insert (buffer trades)
            # TODO: Implement batching for performance
            
            # Publish to stream
            await self.redis_streams.publish(
                RedisStreamsClient.TRADES,
                trade
            )
        
        await exchange.subscribe_trades(symbol, on_trade)
        
        sub_key = f"{exchange_id}:{symbol}:trades"
        self.subscriptions[sub_key] = True
    
    # ==========================================
    # ORDERBOOK
    # ==========================================
    
    async def subscribe_orderbook(
        self,
        exchange_id: str,
        symbol: str
    ):
        """Subscribe to orderbook stream."""
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            raise ValueError(f"Exchange {exchange_id} not found")
        
        async def on_orderbook(orderbook_data):
            # Publish to stream (don't store all snapshots)
            await self.redis_streams.publish(
                RedisStreamsClient.ORDERBOOK,
                {
                    'exchange': exchange_id,
                    'symbol': symbol,
                    'bids': orderbook_data['bids'][:10],  # Top 10
                    'asks': orderbook_data['asks'][:10],
                    'timestamp': orderbook_data['timestamp']
                }
            )
        
        await exchange.subscribe_orderbook(symbol, on_orderbook)
        
        sub_key = f"{exchange_id}:{symbol}:orderbook"
        self.subscriptions[sub_key] = True
    
    # ==========================================
    # BATCH SUBSCRIBE
    # ==========================================
    
    async def subscribe_symbols(
        self,
        exchange_id: str,
        symbols: List[str],
        timeframes: List[str] = ['1h'],
        include_trades: bool = False,
        include_orderbook: bool = False
    ):
        """
        Subscribe to multiple symbols at once.
        """
        logger.info(
            f"Subscribing to {len(symbols)} symbols on {exchange_id}"
        )
        
        tasks = []
        
        for symbol in symbols:
            # Candles
            for timeframe in timeframes:
                tasks.append(
                    self.subscribe_candles(exchange_id, symbol, timeframe)
                )
            
            # Trades
            if include_trades:
                tasks.append(
                    self.subscribe_trades(exchange_id, symbol)
                )
            
            # Orderbook
            if include_orderbook:
                tasks.append(
                    self.subscribe_orderbook(exchange_id, symbol)
                )
        
        await asyncio.gather(*tasks)
        
        logger.info(f"Subscribed to {len(tasks)} streams")


#### 2. **Liquidations Feed** (`market_data/feeds/liquidations_feed.py`)

```python
# market_data/feeds/liquidations_feed.py

import websockets
import json
from datetime import datetime
from decimal import Decimal
import asyncio
import logging

logger = logging.getLogger(__name__)

class LiquidationsFeed:
    """
    Monitor liquidations on Binance Futures.
    
    Liquidations indicate important price levels.
    """
    
    def __init__(
        self,
        redis_streams: RedisStreamsClient,
        db_client: TimescaleDBClient,
        min_size_usd: float = 50000
    ):
        self.redis_streams = redis_streams
        self.db = db_client
        self.min_size_usd = min_size_usd
        
        self.ws_url = "wss://fstream.binance.com/ws/!forceOrder@arr"
        self.ws = None
        self.running = False
        
        # Track liquidation zones
        self.zones = {}  # price_level -> total_usd
    
    async def start(self):
        """Start liquidations feed."""
        self.running = True
        
        asyncio.create_task(self._connect_and_stream())
        
        logger.info("Liquidations feed started")
    
    async def stop(self):
        """Stop liquidations feed."""
        self.running = False
        
        if self.ws:
            await self.ws.close()
        
        logger.info("Liquidations feed stopped")
    
    async def _connect_and_stream(self):
        """Connect to WebSocket and stream liquidations."""
        while self.running:
            try:
                async with websockets.connect(self.ws_url) as ws:
                    self.ws = ws
                    logger.info("Connected to liquidations feed")
                    
                    async for message in ws:
                        data = json.loads(message)
                        
                        # Process liquidations
                        for liq_data in data.get('o', []):
                            await self._process_liquidation(liq_data)
                
            except Exception as e:
                logger.error(f"Liquidations feed error: {e}")
                
                if self.running:
                    # Reconnect after delay
                    await asyncio.sleep(5)
    
    async def _process_liquidation(self, data: Dict):
        """Process single liquidation event."""
        # Parse liquidation
        symbol = data['s']
        side = 'long' if data['S'] == 'SELL' else 'short'
        price = Decimal(data['p'])
        quantity = Decimal(data['q'])
        quantity_usd = quantity * price
        
        # Filter by size
        if quantity_usd < self.min_size_usd:
            return
        
        # Create liquidation event
        liquidation = {
            'time': datetime.fromtimestamp(data['T'] / 1000),
            'symbol': symbol,
            'exchange': 'binance',
            'side': side,
            'price': price,
            'quantity': quantity,
            'quantity_usd': quantity_usd
        }
        
        # Store in DB
        await self.db.insert_liquidation(liquidation)
        
        # Publish to stream
        await self.redis_streams.publish(
            RedisStreamsClient.LIQUIDATIONS,
            liquidation
        )
        
        # Track zone
        await self._track_zone(symbol, price, quantity_usd)
        
        # Alert if large
        if quantity_usd > 1_000_000:
            logger.warning(
                f"🚨 LARGE LIQUIDATION: {symbol} ${quantity_usd:,.0f} "
                f"at {price} ({side})"
            )
    
    async def _track_zone(
        self,
        symbol: str,
        price: Decimal,
        quantity_usd: Decimal
    ):
        """Track liquidation zones."""
        # Round to nearest 100 (for BTC) or adjust per symbol
        price_level = int(price / 100) * 100
        
        key = f"{symbol}:{price_level}"
        
        if key not in self.zones:
            self.zones[key] = {
                'total_usd': Decimal(0),
                'count': 0
            }
        
        self.zones[key]['total_usd'] += quantity_usd
        self.zones[key]['count'] += 1
        
        # Alert if zone > $5M
        if self.zones[key]['total_usd'] > 5_000_000:
            logger.warning(
                f"💀 LIQUIDATION ZONE: {symbol} at {price_level} "
                f"= ${self.zones[key]['total_usd']:,.0f} "
                f"({self.zones[key]['count']} liquidations)"
            )
    
    def get_top_zones(self, symbol: str, limit: int = 10) -> List[Dict]:
        """Get top liquidation zones for symbol."""
        symbol_zones = [
            {
                'price_level': int(key.split(':')[1]),
                'total_usd': zone['total_usd'],
                'count': zone['count']
            }
            for key, zone in self.zones.items()
            if key.startswith(f"{symbol}:")
        ]
        
        # Sort by total USD
        symbol_zones.sort(key=lambda x: x['total_usd'], reverse=True)
        
        return symbol_zones[:limit]


#### 3. **Data Normalizer** (`market_data/processors/normalizer.py`)

```python
# market_data/processors/normalizer.py

from typing import Dict, Any
from decimal import Decimal
from datetime import datetime

class MarketDataNormalizer:
    """
    Normalize market data from different exchanges.
    
    Each exchange has different formats.
    This normalizes to standard format.
    """
    
    @staticmethod
    def normalize_candle(exchange: str, raw_data: Dict) -> Dict:
        """
        Normalize candle data.
        
        Standard format:
        {
            'timestamp': datetime,
            'open': Decimal,
            'high': Decimal,
            'low': Decimal,
            'close': Decimal,
            'volume': Decimal
        }
        """
        if exchange == 'binance':
            return {
                'timestamp': datetime.fromtimestamp(raw_data['t'] / 1000),
                'open': Decimal(raw_data['o']),
                'high': Decimal(raw_data['h']),
                'low': Decimal(raw_data['l']),
                'close': Decimal(raw_data['c']),
                'volume': Decimal(raw_data['v'])
            }
        
        # Add other exchanges...
        
        return raw_data
    
    @staticmethod
    def normalize_trade(exchange: str, raw_data: Dict) -> Dict:
        """
        Normalize trade data.
        
        Standard format:
        {
            'timestamp': datetime,
            'price': Decimal,
            'quantity': Decimal,
            'side': 'buy' or 'sell'
        }
        """
        if exchange == 'binance':
            return {
                'timestamp': datetime.fromtimestamp(raw_data['T'] / 1000),
                'price': Decimal(raw_data['p']),
                'quantity': Decimal(raw_data['q']),
                'side': 'buy' if not raw_data['m'] else 'sell'
            }
        
        return raw_data
    
    @staticmethod
    def normalize_orderbook(exchange: str, raw_data: Dict) -> Dict:
        """
        Normalize orderbook data.
        
        Standard format:
        {
            'bids': [[price, quantity], ...],
            'asks': [[price, quantity], ...],
            'timestamp': datetime
        }
        """
        if exchange == 'binance':
            return {
                'bids': [
                    [Decimal(p), Decimal(q)] 
                    for p, q in raw_data['bids']
                ],
                'asks': [
                    [Decimal(p), Decimal(q)] 
                    for p, q in raw_data['asks']
                ],
                'timestamp': datetime.fromtimestamp(raw_data['E'] / 1000)
            }
        
        return raw_data


#### 4. **Historical Data Downloader** (`scripts/download_historical_data.py`)

```python
# scripts/download_historical_data.py

import asyncio
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
import logging

console = Console()
logger = logging.getLogger(__name__)

class HistoricalDataDownloader:
    """
    Download historical market data.
    
    Supports:
    - Multiple symbols
    - Multiple timeframes
    - Date ranges
    - Resume capability
    """
    
    def __init__(
        self,
        exchange: BaseExchange,
        output_dir: str = 'data/historical'
    ):
        self.exchange = exchange
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def download(
        self,
        symbols: List[str],
        timeframes: List[str],
        start_date: str,
        end_date: Optional[str] = None
    ):
        """
        Download historical data.
        
        Args:
            symbols: ['BTC/USDT', 'ETH/USDT']
            timeframes: ['1h', '4h', '1d']
            start_date: '2022-01-01'
            end_date: '2024-12-01' (optional, defaults to now)
        """
        await self.exchange.connect()
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.utcnow()
        
        console.print(
            f"\n📊 Downloading historical data\n"
            f"Symbols: {len(symbols)}\n"
            f"Timeframes: {timeframes}\n"
            f"Period: {start_date} to {end.strftime('%Y-%m-%d')}\n",
            style="bold cyan"
        )
        
        with Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            for symbol in symbols:
                for timeframe in timeframes:
                    task = progress.add_task(
                        f"[cyan]{symbol} {timeframe}...",
                        total=None
                    )
                    
                    try:
                        candles = await self._download_symbol_timeframe(
                            symbol,
                            timeframe,
                            start,
                            end
                        )
                        
                        # Save to CSV
                        filename = f"{symbol.replace('/', '')}_{timeframe}.csv"
                        filepath = self.output_dir / filename
                        
                        df = pd.DataFrame(candles)
                        df.to_csv(filepath, index=False)
                        
                        progress.update(
                            task,
                            completed=100,
                            description=f"[green]✓ {symbol} {timeframe} ({len(candles)} candles)"
                        )
                        
                    except Exception as e:
                        progress.update(
                            task,
                            description=f"[red]✗ {symbol} {timeframe} - {str(e)}"
                        )
                        logger.error(f"Error downloading {symbol} {timeframe}: {e}")
        
        await self.exchange.disconnect()
        
        console.print("\n✅ Download complete!", style="bold green")
    
    async def _download_symbol_timeframe(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime
    ) -> List[Dict]:
        """Download all candles for symbol/timeframe."""
        all_candles = []
        current = start
        
        # Determine batch size based on timeframe
        batch_sizes = {
            '1m': timedelta(days=1),
            '5m': timedelta(days=5),
            '15m': timedelta(days=15),
            '1h': timedelta(days=30),
            '4h': timedelta(days=120),
            '1d': timedelta(days=365)
        }
        batch_size = batch_sizes.get(timeframe, timedelta(days=30))
        
        while current < end:
            batch_end = min(current + batch_size, end)
            
            # Fetch candles
            candles = await self.exchange.get_candles(
                symbol,
                timeframe,
                since=current,
                limit=1000
            )
            
            if not candles:
                break
            
            all_candles.extend(candles)
            
            # Move to next batch
            last_timestamp = candles[-1]['timestamp']
            current = last_timestamp + timedelta(seconds=1)
            
            # Rate limit
            await asyncio.sleep(0.1)
        
        # Remove duplicates
        seen = set()
        unique_candles = []
        for candle in all_candles:
            ts = candle['timestamp']
            if ts not in seen:
                seen.add(ts)
                unique_candles.append(candle)
        
        return unique_candles


# Usage
if __name__ == '__main__':
    async def main():
        from infrastructure.exchanges.exchange_factory import ExchangeFactory
        
        # Create exchange
        exchange = ExchangeFactory.create(
            'binance',
            api_key='',  # Not needed for public data
            api_secret='',
            testnet=False,
            futures=True
        )
        
        # Download
        downloader = HistoricalDataDownloader(exchange)
        
        await downloader.download(
            symbols=[
                'BTC/USDT',
                'ETH/USDT',
                'SOL/USDT',
                'AVAX/USDT',
                'MATIC/USDT'
            ],
            timeframes=['1h', '4h', '1d'],
            start_date='2022-01-01',
            end_date='2024-12-01'
        )
    
    asyncio.run(main())


### **Criterios de Aceptación**:
- ✅ Market data pipeline procesa 10k+ updates/s
- ✅ Liquidations feed funciona 24/7
- ✅ Data normalizada entre exchanges
- ✅ Historical downloader funciona
- ✅ Data stored en TimescaleDB
- ✅ Redis cache updated en real-time
- ✅ No data gaps detectados
- ✅ Memory usage estable (<1GB para 50 symbols)

### **Entregables**:
- Market data feed manager
- Liquidations feed
- Data normalizer
- Historical downloader
- 3+ años de data descargada
- 20+ tests
- Performance benchmarks

---

## 🧪 FASE 4: BACKTESTING SYSTEM (Semana 5-6)

## **Sprint 4.1: Backtesting Engine Core**
**Duración**: 4-5 días

### Tareas:

#### 1. **Backtest Engine** (`backtesting/engine/backtest_engine.py`)

```python
# backtesting/engine/backtest_engine.py

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BacktestEngine:
    """
    Vectorized backtesting engine.
    
    Features:
    - Fast vectorized operations
    - Realistic commission/slippage
    - Multiple position sizing methods
    - Walk-forward optimization support
    """
    
    def __init__(
        self,
        strategy,
        data: pd.DataFrame,
        initial_capital: float = 10000,
        commission: float = 0.0004,
        slippage: float = 0.0005,
        position_size: str = 'fixed',  # 'fixed', 'risk', 'kelly'
        max_position_size: float = 0.95
    ):
        self.strategy = strategy
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.position_size_method = position_size
        self.max_position_size = max_position_size
        
        # Results
        self.trades = []
        self.equity_curve = []
        self.positions_history = []
    
    def run(self) -> Dict:
        """
        Run backtest.
        
        Returns:
            Dictionary with results and metrics
        """
        logger.info("Starting backtest...")
        
        # Initialize
        capital = self.initial_capital
        position = None
        equity = [capital]
        
        # Iterate through data
        for i in range(len(self.data)):
            current_candle = self.data.iloc[i]
            
            # Check if have position
            if position is not None:
                # Update position
                current_price = current_candle['close']
                position['current_price'] = current_price
                position['unrealized_pnl'] = self._calculate_pnl(position, current_price)
                
                # Check exit conditions
                if self._should_exit(position, current_candle):
                    # Close position
                    capital = self._close_position(position, current_candle, capital)
                    position = None
            
            else:
                # Check entry conditions
                signal = self.strategy.generate_signal(self.data.iloc[:i+1])
                
                if signal and signal['action'] == 'buy':
                    # Open position
                    position = self._open_position(signal, current_candle, capital)
                    
                    if position:
                        capital -= position['cost']
            
            # Update equity
            current_equity = capital
            if position:
                current_equity += position['unrealized_pnl']
            
            equity.append(current_equity)
        
        # Close any remaining position
        if position:
            capital = self._close_position(position, self.data.iloc[-1], capital)
        
        self.equity_curve = equity
        
        # Calculate metrics
        metrics = self._calculate_metrics()
        
        logger.info(f"Backtest complete. Final capital: ${capital:.2f}")
        
        return {
            'initial_capital': self.initial_capital,
            'final_capital': capital,
            'total_return': (capital - self.initial_capital) / self.initial_capital,
            'trades': self.trades,
            'equity_curve': equity,
            'metrics': metrics
        }
    
    def _open_position(
        self,
        signal: Dict,
        candle: pd.Series,
        capital: float
    ) -> Optional[Dict]:
        """Open a new position."""
        entry_price = candle['close'] * (1 + self.slippage)
        
        # Calculate position size
        size = self._calculate_position_size(
            signal,
            entry_price,
            capital
        )
        
        if size <= 0:
            return None
        
        # Calculate cost
        cost = size * entry_price
        commission_cost = cost * self.commission
        total_cost = cost + commission_cost
        
        if total_cost > capital * self.max_position_size:
            return None
        
        position = {
            'entry_time': candle.name,
            'entry_price': entry_price,
            'size': size,
            'cost': total_cost,
            'stop_loss': signal.get('stop_loss'),
            'take_profit': signal.get('take_profit'),
            'current_price': entry_price,
            'unrealized_pnl': 0
        }
        
       logger.debug(
            f"Opened position: {size:.4f} @ {entry_price:.2f} "
            f"(SL: {position['stop_loss']:.2f}, "
            f"TP: {position['take_profit']:.2f})"
            return position

def _close_position(
    self,
    position: Dict,
    candle: pd.Series,
    capital: float
) -> float:
    """Close position and return updated capital."""
    exit_price = candle['close'] * (1 - self.slippage)
    
    # Calculate P&L
    pnl = (exit_price - position['entry_price']) * position['size']
    commission_cost = (position['cost'] + exit_price * position['size']) * self.commission
    net_pnl = pnl - commission_cost
    
    # Update capital
    new_capital = capital + position['cost'] + net_pnl
    
    # Record trade
    trade = {
        'entry_time': position['entry_time'],
        'exit_time': candle.name,
        'entry_price': position['entry_price'],
        'exit_price': exit_price,
        'size': position['size'],
        'pnl': net_pnl,
        'return': net_pnl / position['cost'],
        'duration': (candle.name - position['entry_time']).total_seconds() / 3600  # hours
    }
    
    self.trades.append(trade)
    
    logger.debug(
        f"Closed position: {position['size']:.4f} @ {exit_price:.2f} "
        f"P&L: ${net_pnl:.2f}"
    )
    
    return new_capital

def _should_exit(self, position: Dict, candle: pd.Series) -> bool:
    """Check if should exit position."""
    current_price = candle['close']
    
    # Stop loss
    if position['stop_loss'] and current_price <= position['stop_loss']:
        return True
    
    # Take profit
    if position['take_profit'] and current_price >= position['take_profit']:
        return True
    
    # Strategy exit signal
    signal = self.strategy.generate_signal(self.data.loc[:candle.name])
    if signal and signal['action'] == 'sell':
        return True
    
    return False

def _calculate_position_size(
    self,
    signal: Dict,
    entry_price: float,
    capital: float
) -> float:
    """Calculate position size based on method."""
    if self.position_size_method == 'fixed':
        # Fixed percentage of capital
        return (capital * self.max_position_size) / entry_price
    
    elif self.position_size_method == 'risk':
        # Risk-based sizing
        risk_per_trade = capital * 0.01  # 1% risk
        stop_loss = signal.get('stop_loss', entry_price * 0.95)
        risk_per_unit = entry_price - stop_loss
        
        if risk_per_unit <= 0:
            return 0
        
        size = risk_per_trade / risk_per_unit
        max_size = (capital * self.max_position_size) / entry_price
        
        return min(size, max_size)
    
    elif self.position_size_method == 'kelly':
        # Kelly criterion (advanced)
        # TODO: Implement Kelly criterion
        return (capital * 0.5) / entry_price
    
    return 0

def _calculate_pnl(self, position: Dict, current_price: float) -> float:
    """Calculate unrealized P&L."""
    return (current_price - position['entry_price']) * position['size']

def _calculate_metrics(self) -> Dict:
    """Calculate performance metrics."""
    if not self.trades:
        return {}
    
    trades_df = pd.DataFrame(self.trades)
    equity_series = pd.Series(self.equity_curve)
    
    # Returns
    total_return = (equity_series.iloc[-1] - equity_series.iloc[0]) / equity_series.iloc[0]
    
    # Win rate
    winning_trades = trades_df[trades_df['pnl'] > 0]
    losing_trades = trades_df[trades_df['pnl'] <= 0]
    win_rate = len(winning_trades) / len(trades_df)
    
    # Profit factor
    total_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
    total_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 1
    profit_factor = total_profit / total_loss if total_loss > 0 else 0
    
    # Average win/loss
    avg_win = winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0
    avg_loss = losing_trades['pnl'].mean() if len(losing_trades) > 0 else 0
    
    # Sharpe ratio
    returns = equity_series.pct_change().dropna()
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
    
    # Sortino ratio
    downside_returns = returns[returns < 0]
    sortino = (returns.mean() / downside_returns.std()) * np.sqrt(252) if len(downside_returns) > 0 and downside_returns.std() > 0 else 0
    
    # Max drawdown
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Calmar ratio
    annual_return = total_return * (252 / len(equity_series))
    calmar = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    return {
        'total_return': total_return,
        'num_trades': len(trades_df),
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'sharpe_ratio': sharpe,
        'sortino_ratio': sortino,
        'max_drawdown': max_drawdown,
        'calmar_ratio': calmar,
        'avg_trade_duration': trades_df['duration'].mean()
    }

    2. Strategy Adapter for Backtest (backtesting/strategy_adapter.py)
python# backtesting/strategy_adapter.py

import pandas as pd
from typing import Optional, Dict

class BacktestStrategyAdapter:
    """
    Adapter to make live strategies work with backtest engine.
    """
    
    def __init__(self, strategy_class, **params):
        self.strategy = strategy_class(**params)
        self.params = params
    
    def generate_signal(self, data: pd.DataFrame) -> Optional[Dict]:
        """
        Generate signal from historical data.
        
        Args:
            data: Historical OHLCV data up to current point
        
        Returns:
            Signal dict or None
        """
        # Convert DataFrame to format expected by strategy
        if len(data) < 20:  # Need minimum data
            return None
        
        # Call strategy logic
        signals = self.strategy.on_candle(data.iloc[-1])
        
        if signals and len(signals) > 0:
            signal = signals[0]
            return {
                'action': 'buy' if signal.side == 'buy' else 'sell',
                'price': signal.entry_price,
                'stop_loss': signal.stop_loss,
                'take_profit': signal.take_profit,
                'confidence': signal.confidence
            }
        
        return None


#### 3. **Walk-Forward Optimization** (`backtesting/optimization/walk_forward.py`)
```python
# backtesting/optimization/walk_forward.py

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class WalkForwardOptimizer:
    """
    Walk-forward optimization.
    
    Process:
    1. Split data into train/test windows
    2. Optimize on train window
    3. Test on out-of-sample test window
    4. Roll forward and repeat
    
    Prevents overfitting.
    """
    
    def __init__(
        self,
        strategy_class,
        data: pd.DataFrame,
        param_grid: Dict,
        train_period_days: int = 180,
        test_period_days: int = 60,
        step_days: int = 30
    ):
        self.strategy_class = strategy_class
        self.data = data
        self.param_grid = param_grid
        self.train_period = timedelta(days=train_period_days)
        self.test_period = timedelta(days=test_period_days)
        self.step = timedelta(days=step_days)
        
        self.results = []
    
    def optimize(self, objective: str = 'sharpe_ratio') -> Dict:
        """
        Run walk-forward optimization.
        
        Args:
            objective: Metric to optimize ('sharpe_ratio', 'total_return', etc.)
        
        Returns:
            Results dictionary
        """
        logger.info("Starting walk-forward optimization...")
        
        # Generate windows
        windows = self._generate_windows()
        
        logger.info(f"Generated {len(windows)} windows")
        
        for i, (train_start, train_end, test_start, test_end) in enumerate(windows):
            logger.info(
                f"Window {i+1}/{len(windows)}: "
                f"Train {train_start.date()} to {train_end.date()}, "
                f"Test {test_start.date()} to {test_end.date()}"
            )
            
            # Get train data
            train_data = self.data.loc[train_start:train_end]
            
            # Optimize on train
            best_params = self._optimize_window(train_data, objective)
            
            # Test on out-of-sample
            test_data = self.data.loc[test_start:test_end]
            test_result = self._test_params(test_data, best_params)
            
            self.results.append({
                'window': i + 1,
                'train_start': train_start,
                'train_end': train_end,
                'test_start': test_start,
                'test_end': test_end,
                'best_params': best_params,
                'test_result': test_result
            })
            
            logger.info(
                f"Window {i+1} - Test Sharpe: {test_result['sharpe_ratio']:.2f}, "
                f"Return: {test_result['total_return']:.2%}"
            )
        
        # Aggregate results
        aggregate = self._aggregate_results()
        
        logger.info("Walk-forward optimization complete")
        
        return {
            'windows': self.results,
            'aggregate': aggregate
        }
    
    def _generate_windows(self) -> List[Tuple]:
        """Generate train/test windows."""
        windows = []
        
        start = self.data.index[0]
        end = self.data.index[-1]
        
        current = start
        
        while current + self.train_period + self.test_period <= end:
            train_start = current
            train_end = current + self.train_period
            test_start = train_end
            test_end = test_start + self.test_period
            
            windows.append((train_start, train_end, test_start, test_end))
            
            # Move forward
            current += self.step
        
        return windows
    
    def _optimize_window(self, train_data: pd.DataFrame, objective: str) -> Dict:
        """Optimize parameters on training window."""
        best_score = -np.inf
        best_params = None
        
        # Generate parameter combinations
        param_combinations = self._generate_param_combinations()
        
        for params in param_combinations:
            # Run backtest with these params
            engine = BacktestEngine(
                strategy=BacktestStrategyAdapter(self.strategy_class, **params),
                data=train_data
            )
            
            result = engine.run()
            
            # Get objective score
            score = result['metrics'].get(objective, 0)
            
            if score > best_score:
                best_score = score
                best_params = params
        
        return best_params
    
    def _test_params(self, test_data: pd.DataFrame, params: Dict) -> Dict:
        """Test parameters on out-of-sample data."""
        engine = BacktestEngine(
            strategy=BacktestStrategyAdapter(self.strategy_class, **params),
            data=test_data
        )
        
        result = engine.run()
        
        return result['metrics']
    
    def _generate_param_combinations(self) -> List[Dict]:
        """Generate all parameter combinations from grid."""
        keys = list(self.param_grid.keys())
        values = list(self.param_grid.values())
        
        combinations = []
        
        def generate(index, current):
            if index == len(keys):
                combinations.append(current.copy())
                return
            
            for value in values[index]:
                current[keys[index]] = value
                generate(index + 1, current)
        
        generate(0, {})
        
        return combinations
    
    def _aggregate_results(self) -> Dict:
        """Aggregate results across all windows."""
        if not self.results:
            return {}
        
        # Extract test results
        test_results = [w['test_result'] for w in self.results]
        
        # Calculate averages
        avg_sharpe = np.mean([r['sharpe_ratio'] for r in test_results])
        avg_return = np.mean([r['total_return'] for r in test_results])
        avg_max_dd = np.mean([r['max_drawdown'] for r in test_results])
        avg_win_rate = np.mean([r['win_rate'] for r in test_results])
        
        # Consistency (std dev of returns)
        return_std = np.std([r['total_return'] for r in test_results])
        
        return {
            'avg_sharpe_ratio': avg_sharpe,
            'avg_total_return': avg_return,
            'avg_max_drawdown': avg_max_dd,
            'avg_win_rate': avg_win_rate,
            'return_consistency': 1 / (1 + return_std),  # Higher is better
            'num_windows': len(self.results)
        }


### **Criterios de Aceptación**:
- ✅ Backtest 1 año en <5 min
- ✅ Metrics calculados correctamente
- ✅ Commission/slippage aplicados
- ✅ Walk-forward optimization funciona
- ✅ Results match manual calculation
- ✅ Memory usage <2GB para 1 año
- ✅ 30+ unit tests

### **Entregables**:
- Backtest engine completo
- Strategy adapter
- Walk-forward optimizer
- Performance metrics calculator
- Heat map generator (pendiente)
- 30+ tests
- Sample backtest reports

# 🎯 CONTINUACIÓN ROADMAP (SIN CÓDIGO)

---

## **Sprint 4.2: Optimization & Validation**
**Duración**: 2-3 días

### Tareas:

1. **Grid Search Optimizer**
   - Implementar búsqueda exhaustiva de parámetros
   - Paralelización con multiprocessing (8+ cores)
   - Cache de resultados intermedios
   - Progress tracking con rich
   - Heat map visualization (matplotlib/seaborn)
   - Top N parameter sets ranking
   - Overfitting detection (IS vs OOS spread)

2. **Monte Carlo Simulation**
   - Resample trades con reemplazo
   - 1000+ simulaciones
   - Confidence intervals (95%, 99%)
   - Probability of ruin calculation
   - Distribution plots
   - Worst-case scenario analysis

3. **Multi-Symbol Backtester**
   - Test strategy en 5+ symbols simultáneamente
   - Aggregate results
   - Symbol correlation analysis
   - Survivorship bias detection
   - Report inconsistent performance
   - Identify overfitting (works on 1 symbol only)

4. **Out-of-Sample Validator**
   - Reserve 20-30% data for OOS
   - Never touch test set during optimization
   - Compare IS vs OOS metrics
   - Flag if OOS < 70% of IS performance
   - Statistical tests (t-test, bootstrapping)

### **Criterios de Aceptación**:
- ✅ Grid search 400+ combinations en <30 min
- ✅ Monte Carlo 1000 sims en <2 min
- ✅ Multi-symbol results aggregated
- ✅ OOS validation automatic
- ✅ Heat maps generados
- ✅ Overfitting detectado automáticamente

---

## **Sprint 4.3: Reporting & Visualization**
**Duración**: 2 días

### Tareas:

1. **HTML Report Generator**
   - Template con Jinja2
   - Summary section (metrics table)
   - Equity curve plot (matplotlib → base64)
   - Drawdown chart
   - Monthly returns heatmap
   - Trade distribution histogram
   - Entry/exit markers on price chart
   - Parameter sensitivity charts
   - CSS styling (clean, professional)
   - Export to HTML file

2. **Performance Metrics Library**
   - Returns (total, annual, monthly)
   - Risk metrics (Sharpe, Sortino, Calmar)
   - Drawdown analysis (max, avg, recovery time)
   - Trade metrics (win rate, profit factor, expectancy)
   - Duration analysis (avg holding time)
   - Consecutive wins/losses streaks
   - Risk-adjusted returns

3. **Comparison Tool**
   - Compare multiple backtests side-by-side
   - Strategy A vs Strategy B vs Buy & Hold
   - Metrics comparison table
   - Overlay equity curves
   - Statistical significance tests

### **Criterios de Aceptación**:
- ✅ HTML reports generated automáticamente
- ✅ All charts embedded
- ✅ Reports son legibles y útiles
- ✅ Can compare 3+ strategies
- ✅ Export to PDF (opcional)

---

## 🛡️ FASE 5: RISK MANAGEMENT (Semana 7)

## **Sprint 5.1: Pre-Trade Validation**
**Duración**: 3 días

### Tareas:

1. **Comprehensive Order Validator**
   - Duplicate order check (same symbol, similar price, same side)
   - Existing position check (prevent double entries)
   - Position size limit (max 10% capital per trade)
   - Leverage limit (max 3x)
   - Daily loss limit check (circuit breaker if -5%)
   - SL/TP mandatory validation (CRITICAL)
   - Price decimals validation (exchange-specific)
   - Size decimals validation (exchange-specific)
   - Available capital check
   - Correlation risk check (max 3 correlated positions)
   - Validation result with clear reasons
   - <10ms validation time
   - 100% coverage en critical checks

2. **Individual Risk Checks**
   - PositionLimitCheck: Max size, max positions
   - ExposureCheck: Total exposure across all positions
   - CapitalCheck: Available balance verification
   - CorrelationCheck: Asset correlation matrix
   - LeverageCheck: Margin requirements
   - TimeCheck: Trading hours restrictions
   - MarketConditionCheck: Volatility filters

3. **Risk Configuration**
   - YAML config per environment (dev/prod)
   - Max position size: $1000 (start small)
   - Max total exposure: $5000
   - Max positions: 3
   - Max leverage: 3x
   - Daily loss limit: -5%
   - Stop loss: MANDATORY
   - Take profit: MANDATORY
   - Environment-specific overrides

### **Criterios de Aceptación**:
- ✅ Todos los checks implementados
- ✅ Invalid orders rechazadas con razón clara
- ✅ <10ms validation time
- ✅ Zero false negatives (no risky order passes)
- ✅ Configurable por environment
- ✅ 50+ unit tests

---

## **Sprint 5.2: In-Trade Risk Management**
**Duración**: 2 días

### Tareas:

1. **Stop Loss Manager**
   - Monitor open positions continuamente
   - Track SL levels en real-time
   - Execute SL orders automáticamente
   - Trailing stop logic (optional)
   - Breakeven adjustment después de X% profit
   - Partial close at milestones
   - Emergency stop on connection loss

2. **Circuit Breakers**
   - DailyLossLimitBreaker: Stop trading if -5% día
   - VolatilityBreaker: Pause si volatility > 3x normal
   - LatencyBreaker: Pause si latency > 500ms
   - ConnectionBreaker: Pause si disconnected
   - LiquidationBreaker: Alert en mass liquidations
   - ManualBreaker: Manual override
   - Auto-resume conditions
   - Notifications on trigger

3. **Portfolio-Level Risk**
   - VaR calculator (Value at Risk 95%, 99%)
   - Real-time Sharpe ratio
   - Beta calculation vs market
   - Position concentration (max 30% in 1 asset)
   - Correlation risk (max 70% correlation entre positions)
   - Heat map de exposure
   - Risk dashboard

### **Criterios de Aceptación**:
- ✅ Circuit breakers funcionan
- ✅ SL ejecutado automáticamente
- ✅ Portfolio risk calculated en <100ms
- ✅ System stops si limits excedidos
- ✅ Alerts sent on breaches
- ✅ 30+ tests

---

## **Sprint 5.3: Position Sizing & Kelly Criterion**
**Duración**: 2 días

### Tareas:

1. **Position Sizing Methods**
   - Fixed: Porcentaje fijo de capital
   - Risk-based: 1% risk por trade
   - Kelly Criterion: Optimal bet size
   - Volatility-adjusted: Scale por ATR
   - Confidence-based: Scale por signal confidence
   - Kelly fraction (half-Kelly, quarter-Kelly)
   - Dynamic adjustment basado en drawdown

2. **Kelly Calculator**
   - Calculate win rate from histórico
   - Calculate avg win/loss ratio
   - Kelly % = (win_rate * avg_win - (1-win_rate) * avg_loss) / avg_win
   - Apply Kelly fraction (0.25x - 0.5x for safety)
   - Re-calculate cada 50 trades
   - Conservative defaults

3. **Risk Metrics Dashboard**
   - Current portfolio risk
   - VaR by position
   - Correlation matrix
   - Leverage breakdown
   - Circuit breaker status
   - Daily P&L vs limit
   - Real-time updates

### **Criterios de Aceptación**:
- ✅ Position sizing configurable
- ✅ Kelly criterion implemented
- ✅ Risk dashboard actualizado en real-time
- ✅ Conservative defaults
- ✅ Never over-leverage

---

## ⚡ FASE 6: ORDER EXECUTION ENGINE (Semana 8)

## **Sprint 6.1: Core Execution** (Ya completado anteriormente con código)

## **Sprint 6.2: Advanced Order Types**
**Duración**: 2 días

### Tareas:

1. **OCO Orders (One-Cancels-Other)**
   - Place TP y SL simultáneamente
   - Cancel opposite cuando uno fills
   - Handle partial fills
   - Binance OCO API integration
   - Fallback si exchange no soporta OCO

2. **Iceberg Orders**
   - Split large orders
   - Execute incrementally
   - Reduce market impact
   - Configurable chunk size

3. **TWAP/VWAP Execution**
   - Time-Weighted Average Price
   - Volume-Weighted Average Price
   - Distribute orders over time/volume
   - Minimize slippage

### **Criterios de Aceptación**:
- ✅ OCO orders funcionan
- ✅ Iceberg orders reduce slippage
- ✅ TWAP execution smooth

---

## 🎯 FASE 7: STRATEGY FRAMEWORK (Semana 9)

## **Sprint 7.1: Base Strategy Classes**
**Duración**: 2 días

### Tareas:

1. **Strategy Interface**
   - Abstract base class
   - on_candle() method
   - on_trade() method
   - calculate_position_size()
   - Indicator caching
   - State management

2. **Indicator Library**
   - SMA, EMA
   - RSI, MACD
   - Bollinger Bands
   - ATR, ADX
   - Volume indicators
   - Custom indicators
   - Caching mechanism

3. **Signal Generation**
   - Signal class con metadata
   - Confidence scoring (0-1)
   - Entry/exit logic
   - SL/TP calculation
   - Validation

---

## **Sprint 7.2: Breakout Strategy (Moon Dev Validated)**
**Duración**: 2 días

### Tareas:

1. **Implementation**
   - Daily resistance (20-day high)
   - Hourly entry (close > resistance)
   - 7% take profit (optimized)
   - 16% stop loss (optimized)
   - Volume confirmation filter
   - Configurable via YAML

2. **Backtesting**
   - Test on BTC, ETH, SOL, INJ, AVAX
   - 2022-2024 period
   - Walk-forward optimization
   - Results documentation
   - Compare vs buy-and-hold

3. **Production Config**
   - Conservative parameters
   - Start with $10 positions
   - Scale plan documented
   - Risk limits configured

---

## 🔍 FASE 8: SCANNER SYSTEM (Semana 10)

## **Sprint 8.1: Scanner Framework**
**Duración**: 2 días

### Tareas:

1. **Base Scanner**
   - Abstract scanner class
   - scan() method returns ScanResult[]
   - Criteria documentation
   - Configurable parameters

2. **Scanner Engine**
   - Orchestrate múltiples scanners
   - Schedule scans (every 60s)
   - Aggregate results
   - Filter duplicates
   - Rank by confidence
   - Store results en DB

3. **Scanner Result**
   - Symbol, entry_price, SL, TP
   - Confidence score
   - Metadata (why detected)
   - Timestamp

---

## **Sprint 8.2: Scanner Implementations**
**Duración**: 3 días

### Tareas:

1. **Breakout Scanner**
   - Scan 100+ symbols
   - Detect breakouts above resistance
   - Volume confirmation
   - Confidence scoring
   - <30s para 100 symbols

2. **Volume Scanner**
   - Detect volume spikes
   - > 2x avg volume
   - Price momentum confirmation

3. **Momentum Scanner**
   - RSI > 60
   - MACD bullish crossover
   - Price above SMAs

4. **Liquidity Scanner (NEW)**
   - Large liquidations detected
   - Price near liquidation zones
   - Potential reversal signals

5. **Regime Scanner (NEW)**
   - Classify current market regime
   - Bull/bear/range/high vol/low vol
   - Enable/disable strategies accordingly

### **Criterios de Aceptación**:
- ✅ Scanner 100 symbols en <30s
- ✅ Confidence scoring útil
- ✅ Results stored en DB
- ✅ CLI tool funciona
- ✅ No false positives excesivos

---

## 🌐 FASE 9: APIs (Internal & External) (Semana 11)

## **Sprint 9.1: Internal REST API**
**Duración**: 3 días

### Tareas:

1. **FastAPI Application**
   - Main app setup
   - CORS middleware
   - Authentication middleware
   - Rate limiting middleware
   - Error handling
   - Request logging

2. **API Endpoints**

**Orders API** (`/api/orders`):
- POST /orders - Place order
- GET /orders - List orders
- GET /orders/{id} - Get order
- DELETE /orders/{id} - Cancel order

**Positions API** (`/api/positions`):
- GET /positions - List positions
- GET /positions/{id} - Get position
- POST /positions/{id}/close - Close position

**Strategies API** (`/api/strategies`):
- GET /strategies - List strategies
- POST /strategies - Deploy strategy
- PUT /strategies/{id} - Update config
- DELETE /strategies/{id} - Stop strategy
- GET /strategies/{id}/performance - Get metrics

**Backtests API** (`/api/backtests`):
- POST /backtests - Run backtest
- GET /backtests - List backtests
- GET /backtests/{id} - Get results
- GET /backtests/{id}/report - HTML report

**Scanner API** (`/api/scanner`):
- POST /scanner/scan - Run scanner
- GET /scanner/results - Recent results
- GET /scanner/results/{id} - Get result

**Risk API** (`/api/risk`):
- GET /risk/portfolio - Portfolio risk
- GET /risk/limits - Current limits
- GET /risk/circuit-breakers - Status

**Health API** (`/api/health`):
- GET /health - System health
- GET /health/exchanges - Exchange status
- GET /health/database - DB status

3. **Pydantic Schemas**
   - Request/response models
   - Validation
   - Documentation auto-generated

### **Criterios de Aceptación**:
- ✅ API responds <50ms p99
- ✅ Authentication working
- ✅ Rate limiting prevents abuse
- ✅ OpenAPI docs auto-generated
- ✅ All endpoints tested

---

## **Sprint 9.2: WebSocket Server**
**Duración**: 2 días

### Tareas:

1. **WebSocket Setup**
   - FastAPI WebSocket support
   - Connection management
   - Heartbeat/ping-pong
   - Reconnection handling

2. **Real-time Streams**
   - Market data stream
   - Order updates stream
   - Position updates stream
   - Portfolio updates stream
   - Scanner results stream
   - System events stream

3. **Subscription Management**
   - Subscribe to specific symbols
   - Subscribe to specific events
   - Unsubscribe
   - Multiple clients support

### **Criterios de Aceptación**:
- ✅ WebSocket stable 24/7
- ✅ <10ms update latency
- ✅ Auto-reconnect works
- ✅ 100+ concurrent connections

---

## **Sprint 9.3: External APIs Integration**
**Duración**: 2 días

### Tareas:

1. **CoinGecko API**
   - Price data
   - Market cap data
   - Historical data
   - Rate limiting

2. **TradingView TA Library**
   - Technical analysis
   - Indicator calculations
   - Chart patterns

3. **News API (optional)**
   - CryptoPanic
   - CoinTelegraph
   - Sentiment analysis
   - Integration con strategy logic

### **Criterios de Aceptación**:
- ✅ All APIs integrated
- ✅ Rate limiting respected
- ✅ Error handling robust
- ✅ Caching implemented

---

## 📊 FASE 10: MONITORING & OBSERVABILITY (Semana 12)

## **Sprint 10.1: Logging System**
**Duración**: 2 días

### Tareas:

1. **Structured Logging**
   - JSON format
   - Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   - Request IDs para tracing
   - Timestamp en UTC
   - Component/module tagging
   - User ID (if authenticated)

2. **Log Handlers**
   - Console handler (development)
   - File handler (rotating, max 100MB)
   - Syslog handler (production)
   - ELK integration (optional)

3. **Log Aggregation**
   - Centralized logging
   - Search capability
   - Filtering
   - Alerts on ERROR/CRITICAL

### **Criterios de Aceptación**:
- ✅ All components logging correctly
- ✅ No sensitive data logged
- ✅ Logs rotated automáticamente
- ✅ Searchable

---

## **Sprint 10.2: Metrics & Prometheus**
**Duración**: 2 días

### Tareas:

1. **Prometheus Integration**
   - Prometheus client library
   - /metrics endpoint
   - Counter, Gauge, Histogram, Summary

2. **System Metrics**
   - orders_placed_total (counter)
   - orders_filled_total (counter)
   - orders_rejected_total (counter)
   - positions_open (gauge)
   - portfolio_value (gauge)
   - api_request_duration_seconds (histogram)
   - market_data_latency_ms (histogram)
   - execution_latency_ms (histogram)

3. **Business Metrics**
   - trades_total (counter)
   - trade_pnl (histogram)
   - daily_pnl (gauge)
   - sharpe_ratio (gauge)
   - max_drawdown (gauge)
   - win_rate (gauge)

4. **Infrastructure Metrics**
   - cpu_usage_percent (gauge)
   - memory_usage_mb (gauge)
   - disk_usage_percent (gauge)
   - database_connections (gauge)
   - redis_connections (gauge)
   - websocket_connections (gauge)

### **Criterios de Aceptación**:
- ✅ Prometheus scraping funciona
- ✅ 50+ metrics tracked
- ✅ Historical data retained
- ✅ Grafana dashboards (next sprint)

---

## **Sprint 10.3: Grafana Dashboards**
**Duración**: 2 días

### Tareas:

1. **System Health Dashboard**
   - CPU/Memory/Disk usage
   - API latency
   - Database performance
   - Redis performance
   - WebSocket connections
   - Error rates

2. **Trading Metrics Dashboard**
   - Open positions count
   - Portfolio value over time
   - Daily P&L
   - Win rate
   - Sharpe ratio
   - Max drawdown
   - Orders per minute
   - Execution latency

3. **Risk Metrics Dashboard**
   - Position sizes
   - Leverage usage
   - VaR over time
   - Circuit breaker status
   - Correlation heatmap
   - Daily loss vs limit

4. **Liquidations Dashboard (NEW)**
   - Liquidations per symbol
   - Large liquidations (>$1M)
   - Liquidation zones heatmap
   - Price vs liquidation levels

5. **Scanner Dashboard (NEW)**
   - Scans per minute
   - Opportunities detected
   - Confidence distribution
   - Top symbols scanned

### **Criterios de Aceptación**:
- ✅ 5+ dashboards creados
- ✅ Real-time updates
- ✅ Alerts configured
- ✅ Mobile-friendly

---

## **Sprint 10.4: Alerting System** (Ya implementado anteriormente)

Reforzar con:
- PagerDuty integration
- Escalation policies
- On-call rotation
- Alert fatigue prevention

---

## 🚀 FASE 11: DEVOPS & INFRASTRUCTURE (Semana 13)

## **Sprint 11.1: Docker & Compose**
**Duración**: 2 días

### Tareas:

1. **Dockerfiles**
   - Dockerfile.python (multi-stage)
   - Dockerfile.cpp (compilation)
   - Optimized image size
   - Layer caching
   - Security scanning

2. **Docker Compose**
   - docker-compose.yml (all services)
   - PostgreSQL (TimescaleDB)
   - Redis
   - Prometheus
   - Grafana
   - Trading system
   - Networks configurados
   - Volumes para persistence

3. **Development Setup**
   - docker-compose.dev.yml
   - Hot reload
   - Debug mode
   - Test database

### **Criterios de Aceptación**:
- ✅ docker-compose up funciona
- ✅ All services start
- ✅ System running en <2 min
- ✅ Logs aggregated

---

## **Sprint 11.2: CI/CD Pipeline**
**Duración**: 2 días

### Tareas:

1. **GitHub Actions**
   - .github/workflows/test.yml
   - .github/workflows/lint.yml
   - .github/workflows/deploy.yml

2. **Test Pipeline**
   - Run unit tests
   - Run integration tests
   - Code coverage report
   - Fail if coverage <80%

3. **Lint Pipeline**
   - black (formatting)
   - flake8 (linting)
   - mypy (type checking)
   - isort (import sorting)

4. **Deploy Pipeline**
   - Build Docker images
   - Push to registry
   - Deploy to staging
   - Run smoke tests
   - Deploy to production (manual approval)

### **Criterios de Aceptación**:
- ✅ All pipelines working
- ✅ Tests run on every PR
- ✅ Deployment automated
- ✅ Rollback capability

---

## **Sprint 11.3: Environment Management**
**Duración**: 2 días

### Tareas:

1. **Environments**
   - Development (local)
   - Staging (cloud)
   - Production (cloud)

2. **Configuration**
   - Environment variables
   - Secrets management (AWS Secrets Manager / Vault)
   - Config per environment
   - No hardcoded credentials

3. **Infrastructure as Code**
   - Terraform configs (optional)
   - AWS/GCP/DO setup
   - VPC configuration
   - Security groups
   - Load balancers

### **Criterios de Aceptación**:
- ✅ 3 environments working
- ✅ Secrets encrypted
- ✅ IaC reproducible
- ✅ Zero manual setup

---

## **Sprint 11.4: Backup & Disaster Recovery**
**Duración**: 1 día

### Tareas:

1. **Database Backups**
   - Automated daily backups
   - Point-in-time recovery
   - Offsite storage
   - Retention policy (30 days)

2. **Config Backups**
   - Strategy configs
   - Risk configs
   - API keys (encrypted)

3. **Disaster Recovery Plan**
   - RTO (Recovery Time Objective): 1 hour
   - RPO (Recovery Point Objective): 15 min
   - Runbook documented
   - Recovery testing

### **Criterios de Aceptación**:
- ✅ Backups automated
- ✅ Restore tested
- ✅ DR plan documented
- ✅ Team trained

---

## 🧪 FASE 12: TESTING STRATEGY (Semana 14)

## **Sprint 12.1: Unit Tests**
**Duración**: 3 días

### Tareas:

1. **Test Coverage**
   - Domain layer: 100%
   - Application layer: 90%
   - Infrastructure layer: 80%
   - pytest framework
   - pytest-asyncio
   - pytest-cov

2. **Test Organization**
   - tests/unit/domain/
   - tests/unit/application/
   - tests/unit/strategies/
   - tests/unit/risk_management/
   - tests/unit/execution/

3. **Mocking**
   - Mock external APIs
   - Mock database
   - Mock Redis
   - Mock exchanges
   - pytest-mock

### **Criterios de Aceptación**:
- ✅ 300+ unit tests
- ✅ >85% code coverage
- ✅ Tests run en <30s
- ✅ Zero flaky tests

---

## **Sprint 12.2: Integration Tests**
**Duración**: 2 días

### Tareas:

1. **Test Scenarios**
   - End-to-end order flow
   - Market data pipeline
   - Strategy execution
   - Scanner pipeline
   - Risk checks
   - Database operations

2. **Test Environment**
   - Docker testnet
   - Test database
   - Mock exchanges
   - Fixtures

3. **Test Data**
   - Sample market data
   - Sample orders
   - Sample positions

### **Criterios de Aceptación**:
- ✅ 50+ integration tests
- ✅ Tests run en <5 min
- ✅ Test DB isolated
- ✅ Cleanup after tests

---

## **Sprint 12.3: Performance & Load Tests**
**Duración**: 2 días

### Tareas:

1. **Performance Tests**
   - Order placement latency
   - Market data throughput
   - Database query speed
   - API response time
   - locust framework

2. **Load Tests**
   - 1000 orders/min
   - 10k market updates/s
   - 100 concurrent API requests
   - Stress testing

3. **Benchmarks**
   - Baseline metrics
   - Regression detection
   - Performance reports

### **Criterios de Aceptación**:
- ✅ <50ms p99 order execution
- ✅ 10k+ market updates/s
- ✅ API <100ms p99
- ✅ System stable under load

---

## **Sprint 12.4: Chaos Engineering**
**Duración**: 1 día

### Tareas:

1. **Chaos Tests**
   - Exchange disconnection
   - Database failure
   - Redis failure
   - Network latency spikes
   - High CPU load
   - Memory pressure

2. **Recovery Testing**
   - Graceful degradation
   - Auto-reconnection
   - Data consistency
   - No data loss

### **Criterios de Aceptación**:
- ✅ System recovers automáticamente
- ✅ No data loss
- ✅ Positions tracked correctly
- ✅ Alerts sent

---

## 🔒 FASE 13: PRODUCTION HARDENING (Semana 15)

## **Sprint 13.1: Security**
**Duración**: 2 días

### Tareas:

1. **Security Audit**
   - Dependency scanning (safety, snyk)
   - Secret scanning
   - SQL injection prevention
   - XSS prevention
   - CSRF protection

2. **Authentication & Authorization**
   - JWT tokens
   - API key rotation
   - Role-based access
   - Rate limiting per user

3. **Encryption**
   - TLS/SSL everywhere
   - Encrypted secrets storage
   - Encrypted database backups

### **Criterios de Aceptación**:
- ✅ No critical vulnerabilities
- ✅ All secrets encrypted
- ✅ Auth working
- ✅ Security scan passed

---

## **Sprint 13.2: Reliability**
**Duración**: 2 días

### Tareas:

1. **Error Handling**
   - Global exception handler
   - Graceful degradation
   - Retry logic everywhere
   - Circuit breakers

2. **Health Checks**
   - Liveness probe
   - Readiness probe
   - Deep health check
   - /health endpoint

3. **Graceful Shutdown**
   - SIGTERM handling
   - Cancel pending orders
   - Close WebSockets
   - Flush buffers
   - Save state

### **Criterios de Aceptación**:
- ✅ No crashes en 48h run
- ✅ Graceful shutdown works
- ✅ Health checks accurate
- ✅ Auto-recovery funciona

---

## **Sprint 13.3: Documentation**
**Duración**: 2 días

### Tareas:

1. **README.md**
   - Project overview
   - Quick start (5 min)
   - Architecture diagram
   - Features list
   - Screenshots

2. **DEPLOYMENT.md**
   - Requirements
   - Step-by-step guide
   - Environment variables
   - Troubleshooting

3. **API Documentation**
   - OpenAPI/Swagger auto-generated
   - Examples for each endpoint
   - Authentication guide
   - Rate limits

4. **Runbook**
   - How to start system
   - How to stop system
   - How to deploy strategy
   - How to handle errors
   - Emergency procedures
   - On-call guide

5. **Strategy Documentation**
   - Each strategy explained
   - Parameters documented
   - Backtest results
   - Known limitations
   - Market conditions

### **Criterios de Aceptación**:
- ✅ Docs completas
- ✅ New team member can setup en <30 min
- ✅ API docs auto-generated
- ✅ Runbook tested

---

## 🎯 FASE 14: ADVANCED FEATURES (Semana 16+)

## **Sprint 14.1: Regime Detection**
**Duración**: 1 semana

### Tareas:

1. **Feature Engineering**
   - Volatility features (VIX, ATR, Bollinger width)
   - Trend features (SMA slopes, ADX)
   - Volume features (OBV, VWAP)
   - Correlation features (BTC correlation)

2. **Regime Classifier**
   - Rule-based (MVP)
   - ML-based (sklearn, XGBoost)
   - 8 regime types (Jim Simons)
   - Confidence scoring

3. **Strategy Mapper**
   - Map regime → optimal strategies
   - Auto-enable/disable strategies
   - Backtest per regime
   - Performance tracking per regime

### **Criterios de Aceptación**:
- ✅ Regime classified en real-time
- ✅ Strategies adapted automatically
- ✅ Performance improved vs no regime detection
- ✅ >70% classification accuracy

---

## **Sprint 14.2: C++ Hot Path (Optional)**
**Duración**: 2+ semanas

### Tareas:

1. **C++ Components**
   - Order executor (<1ms)
   - Market data parser
   - Technical indicators (SMA, EMA, RSI, MACD)
   - Lock-free data structures

2. **Python Bindings**
   - pybind11 wrappers
   - Shared memory IPC
   - Zero-copy data transfer

3. **Benchmarking**
   - Compare Python vs C++
   - Latency reduction
   - Throughput improvement

### **Criterios de Aceptación**:
- ✅ Order execution <1ms p99
- ✅ 10x throughput improvement
- ✅ Python integration seamless
- ✅ No memory leaks

---

## **Sprint 14.3: Machine Learning Strategies**
**Duración**: 2+ semanas

### Tareas:

1. **Feature Engineering**
   - Price features
   - Volume features
   - Technical indicators
   - Market microstructure
   - Alternative data

2. **Model Development**
   - LSTM price prediction
   - Reinforcement learning (DQN, PPO)
   - Ensemble methods
   - Feature importance

3. **Backtesting ML Models**
   - Walk-forward validation
   - Cross-validation
   - Overfitting prevention
   - Reality check

### **Criterios de Aceptación**:
- ✅ Model trained and validated
-