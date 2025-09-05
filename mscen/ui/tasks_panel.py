from __future__ import annotations

import streamlit as st
from pathlib import Path
from ..tasks.queue import TaskQueue, TaskStatus


def tasks_panel(base_dir: Path, submit_cb):
    st.markdown("### 📦 任务队列")
    tq = TaskQueue(base_dir)

    with st.expander("提交新任务"):
        col1, col2 = st.columns(2)
        with col1:
            kind = st.selectbox("任务类型", ["txt2all", "img2music", "music2lights"]) 
            prompt = st.text_input("主题/提示词", placeholder="如：cozy christmas")
        with col2:
            duration = st.slider("时长(秒)", 5, 60, 20)
        if st.button("提交任务", type="primary"):
            t = tq.submit(kind, {"prompt": prompt, "duration": duration})
            submit_cb(t)
            st.success(f"已提交：{t.id}")
            st.rerun()

    tasks = tq.list()
    if not tasks:
        st.info("暂无任务")
        return

    for t in tasks:
        with st.container(border=True):
            st.write(f"ID: {t.id} | 类型: {t.kind}")
            st.progress(t.progress)
            cols = st.columns(5)
            cols[0].metric("状态", t.status)
            cols[1].metric("进度", f"{int(t.progress*100)}%")
            cols[2].metric("错误", t.error or "-")
            if cols[3].button("暂停", key=f"pause_{t.id}"):
                tq.pause(t.id)
                st.rerun()
            if cols[4].button("恢复/重试", key=f"resume_{t.id}"):
                tq.resume(t.id)
                st.rerun() 