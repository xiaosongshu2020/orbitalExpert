# 代码整理中... `(*>﹏<*)′
查看演示视频：https://www.bilibili.com/video/BV1J8Gwz9EnQ
# OrbitExpert AI Agent
### An AI-powered assistant for space mission planning, satellite operations, and orbital analysis. 
### developed by husonghua (lxiahu@hotmail.com)

---

![Orbit Visualization](satelliteScenario/figs/demo1_satellite_orbits.png)


## Key Capabilities

### 1. Satellite Scenario Simulation
- Orbit propagation for LEO, GEO, and GPS satellites
- Ground station visibility analysis
- 3D visualization of satellite orbits and ground tracks
- Multiple observation modes (Azimuth/Elevation, RA/DEC)

### 2. Orbit Prediction & Analysis
- Numerical orbit prediction tools
- Initial orbit determination
- Ephemeris generation and analysis

### 3. Observation Planning
- Ground station access calculation
- Observation data processing
- Time system conversions

### 4. Data Processing
- Earth orientation parameters (EOP)
- Gravity models (GGM03C)
- Atmospheric models (NRLMSISE-00)

## System Components

```
orbitExpert/
├── satelliteScenario/    # Python simulation toolkit
├── src/                  # Core AI agent source code
│   ├── orbitExpert.py    # Main AI agent
│   ├── tool_*.py         # Specialized tools
├── tools/                # Pre-built executables
│   ├── orbitPrediction*.exe
│   ├── observation.exe
│   ├── timeConversion.exe
├── data/                 # Earth and satellite data
│   ├── Earth_*.jpg       # Earth texture maps
│   ├── ephemeris_*.txt   # Satellite ephemeris
├── OPLIB/                # Orbit prediction library
│   ├── files/            # Earth/Space environment data
├── figs/                 # Output visualizations
```

## Installation

1. **Python Environment**:
```bash
pip install -r requirements.txt
```

2. **System Requirements**:
- Windows/Linux/macOS
- Python 3.8+
- 4GB+ RAM recommended for large simulations

## Quick Start

### Using the AI Agent
```bash
python src/orbitExpert.py
```
say to the AI agent:
```
你好，请你仿真一个地面站观测卫星的场景。
首先，请你计算一条LEO卫星的轨道，轨道高度约600km，要考虑20阶次引力场，日月引力，大气阻力，SRP；
然后，在南京市设立一个地面站，使用望远镜观测该卫星，记录方位角、俯仰角数据；
接着，请你绘制卫星轨道的三维图像，再将观测数据可视化；
最后，请你写一个报告，详细介绍本次任务，保存在./report.md;
```

## Data Resources

The system includes:
- Earth orientation parameters (1973-2021)
- High-precision gravity models
- Atmospheric density models
- Multiple world map textures

## License

MIT License

## Support

For issues or feature requests, please open an issue in the project repository.
