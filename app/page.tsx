"use client";

import { useState } from "react";

const tasks = [
  { label: "Test free chlorine and pH", due: "Today · 6:00 PM", tag: "Water" },
  { label: "Empty skimmer baskets", due: "Tomorrow", tag: "Cleaning" },
  { label: "Inspect pump strainer", due: "Sat · 9:00 AM", tag: "Equipment" },
];

export default function Home() {
  const [completed, setCompleted] = useState<number[]>([]);
  const [toast, setToast] = useState("");

  function toggleTask(index: number) {
    setCompleted((current) => current.includes(index) ? current.filter((item) => item !== index) : [...current, index]);
  }

  function recordReading() {
    setToast("Reading form is ready for the next build step.");
    window.setTimeout(() => setToast(""), 2600);
  }

  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Poolside home"><span className="brandMark">P</span><span>Poolside</span></a>
        <nav aria-label="Primary navigation">
          <a className="active" href="#overview">Overview</a><a href="#water">Water</a><a href="#equipment">Equipment</a><a href="#maintenance">Maintenance</a>
        </nav>
        <button className="avatar" aria-label="Open profile">KF</button>
      </header>

      <section className="shell" id="top">
        <div className="hero" id="overview">
          <div><p className="eyebrow">SATURDAY, JULY 18</p><h1>Your pool is ready.</h1><p className="subhead">Water is balanced, equipment is running, and there are no urgent issues.</p></div>
          <div className="heroActions"><span className="status"><i /> All systems normal</span><button className="primary" onClick={recordReading}>+ Record reading</button></div>
        </div>

        <section className="chemistry" id="water" aria-labelledby="chemistry-heading">
          <div className="sectionHeading"><div><p className="eyebrow">WATER CHEMISTRY</p><h2 id="chemistry-heading">Clear, calm, balanced.</h2></div><span className="updated">Updated today at 8:42 AM</span></div>
          <div className="readings">
            <article className="reading featured"><div className="readingTop"><span>Free chlorine</span><span className="pill good">Ideal</span></div><strong>3.2 <small>ppm</small></strong><div className="range"><span style={{ width: "58%" }} /></div><p>Target 2.0–4.0 ppm</p></article>
            <article className="reading"><div className="readingTop"><span>pH</span><span className="pill good">Ideal</span></div><strong>7.5</strong><div className="range"><span style={{ width: "52%" }} /></div><p>Target 7.4–7.6</p></article>
            <article className="reading"><div className="readingTop"><span>Alkalinity</span><span className="pill good">Good</span></div><strong>92 <small>ppm</small></strong><div className="range"><span style={{ width: "46%" }} /></div><p>Target 80–120 ppm</p></article>
            <article className="reading"><div className="readingTop"><span>Water temp</span><span className="pill neutral">Comfortable</span></div><strong>82<small>°F</small></strong><p className="trend">↗ 2° since yesterday</p></article>
          </div>
        </section>

        <div className="lowerGrid">
          <section className="panel" id="equipment">
            <div className="panelHeader"><div><p className="eyebrow">EQUIPMENT</p><h2>Running smoothly</h2></div><button className="textButton">View all →</button></div>
            <div className="equipmentList">
              <div className="equipmentItem"><span className="icon pump">↻</span><div><strong>Variable-speed pump</strong><p>Running · 1,850 RPM</p></div><span className="live">Live</span></div>
              <div className="equipmentItem"><span className="icon">♨</span><div><strong>Pool heater</strong><p>Standby · Set to 82°F</p></div><span className="mutedState">Standby</span></div>
              <div className="equipmentItem"><span className="icon">✦</span><div><strong>Salt system</strong><p>Generating · Output 45%</p></div><span className="live">Live</span></div>
            </div>
          </section>

          <section className="panel" id="maintenance">
            <div className="panelHeader"><div><p className="eyebrow">UP NEXT</p><h2>Keep it sparkling</h2></div><button className="textButton">Full schedule →</button></div>
            <div className="taskList">
              {tasks.map((task, index) => <label className={`task ${completed.includes(index) ? "done" : ""}`} key={task.label}><input type="checkbox" checked={completed.includes(index)} onChange={() => toggleTask(index)} /><span className="check" /><span className="taskCopy"><strong>{task.label}</strong><small>{task.due}</small></span><span className="taskTag">{task.tag}</span></label>)}
            </div>
          </section>
        </div>
        <footer><span>Poolside · Home pool care, made calm.</span><span>Last sync: just now</span></footer>
      </section>
      {toast && <div className="toast" role="status">{toast}</div>}
    </main>
  );
}
