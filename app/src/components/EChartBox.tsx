"use client";

import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";

interface EChartBoxProps {
  option: echarts.EChartsCoreOption;
  height?: string;
  ariaLabel: string;
}

export default function EChartBox({ option, height = "340px", ariaLabel }: EChartBoxProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    if (!chartRef.current) {
      chartRef.current = echarts.init(containerRef.current, undefined, { renderer: "svg" });
    }
    chartRef.current.setOption(option, true);

    const handleResize = () => chartRef.current?.resize();
    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [option]);

  useEffect(() => {
    return () => {
      chartRef.current?.dispose();
      chartRef.current = null;
    };
  }, []);

  return (
    <div
      ref={containerRef}
      style={{ width: "100%", height }}
      role="img"
      aria-label={ariaLabel}
      className="w-full"
    />
  );
}
