import { useState, useRef, useCallback } from 'react'
import Webcam from 'react-webcam'
import Confetti from 'react-confetti'
import './index.css'

const JURY = [
  { id: 'skeptic', name: 'The Skeptic', emoji: '🕵️', desc: 'Analyzes your face', yes: 'REAL', no: 'FAKE' },
  { id: 'doctor', name: 'The Doctor', emoji: '👨‍⚕️', desc: 'Evaluates urgency', yes: 'CRITICAL', no: 'STABLE' },
  { id: 'gambler', name: 'The Gambler', emoji: '🎲', desc: 'Tests your luck', yes: 'IN', no: 'OUT' },
]

function JuryCard({ member, vote, loading }) {
  const isYes = vote === member.yes
  const hasVoted = vote && !['UNKNOWN', 'ERROR'].includes(vote)
  
  return (
    <div className={`jury-card p-5 text-center ${hasVoted ? (isYes ? 'voted-yes' : 'voted-no') : ''}`}>
      <div className="emoji-lg mb-2">{member.emoji}</div>
      <h3 className="font-semibold text-zinc-800">{member.name}</h3>
      <p className="text-xs text-zinc-400 mb-3">{member.desc}</p>
      <div className="h-6">
        {loading ? (
          <span className="text-amber-500 text-sm" style={{animation: 'pulse 1s infinite'}}>Thinking...</span>
        ) : hasVoted ? (
          <span className={`badge ${isYes ? 'badge-success' : 'badge-error'}`}>
            {vote}
          </span>
        ) : (
          <span className="text-zinc-300">—</span>
        )}
      </div>
    </div>
  )
}

function SlotMachine({ spinning, result }) {
  const symbols = result === 'GRANTED' ? ['✅', '✅', '✅'] : 
                  result === 'DENIED' ? ['❌', '❌', '❌'] : ['🎰', '🎰', '🎰']
  
  return (
    <div className="slot-container">
      {symbols.map((s, i) => (
        <div key={i} className={`slot ${spinning ? 'opacity-60' : ''}`}>
          {s}
        </div>
      ))}
    </div>
  )
}

export default function App() {
  const [stage, setStage] = useState('welcome')
  const [plea, setPlea] = useState('')
  const [image, setImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [verdict, setVerdict] = useState(null)
  const [confetti, setConfetti] = useState(false)
  const [shake, setShake] = useState(false)
  const [demo, setDemo] = useState(false)
  const webcamRef = useRef(null)

  const capture = useCallback(() => {
    const shot = webcamRef.current?.getScreenshot()
    if (shot) {
      setImage(shot.split(',')[1])
      setStage('plea')
    }
  }, [])

  const submit = async () => {
    if (!plea.trim()) return
    setLoading(true)
    setStage('deliberating')

    try {
      const res = await fetch('/api/judge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plea, image_base64: image, demo_mode: demo })
      })
      const data = await res.json()
      await new Promise(r => setTimeout(r, 2500))
      
      setVerdict(data)
      setStage('verdict')
      
      if (data.verdict === 'GRANTED') {
        setConfetti(true)
        setTimeout(() => setConfetti(false), 5000)
      } else {
        setShake(true)
        setTimeout(() => setShake(false), 400)
      }
    } catch {
      setVerdict({
        verdict: 'DENIED',
        reasoning: 'Connection error',
        roast: 'The court is offline.',
        jury_votes: { skeptic: 'ERROR', doctor: 'ERROR', gambler: 'ERROR' }
      })
      setStage('verdict')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setStage('welcome')
    setPlea('')
    setImage(null)
    setVerdict(null)
  }

  return (
    <div className={`min-h-screen py-10 px-5 max-w-md mx-auto ${shake ? 'shake' : ''}`}>
      {confetti && <Confetti recycle={false} numberOfPieces={250} />}
      
      {/* Header */}
      <header className="text-center mb-10">
        <div className="emoji-xl mb-2">🚽</div>
        <h1 className="text-2xl font-bold text-zinc-900">Lucky Loo</h1>
        <p className="text-zinc-500 text-sm">The High-Stakes Restroom Finder</p>
        <label className="inline-flex items-center gap-2 mt-4 text-xs text-zinc-400 cursor-pointer select-none">
          <input 
            type="checkbox" 
            checked={demo} 
            onChange={e => setDemo(e.target.checked)}
          />
          Demo Mode
        </label>
      </header>

      {/* Welcome */}
      {stage === 'welcome' && (
        <div className="fade-in">
          <div className="card p-8 text-center mb-8">
            <h2 className="text-lg font-semibold text-zinc-800 mb-2">Prove Your Desperation</h2>
            <p className="text-zinc-500 text-sm mb-6">
              The AI Jury will analyze your face and plea to decide if you deserve access.
            </p>
            <button onClick={() => setStage('camera')} className="btn btn-primary">
              I Need To Go
            </button>
          </div>
          
          <p className="text-center text-zinc-400 text-xs uppercase tracking-wider mb-4">The Jury</p>
          <div className="grid grid-cols-3 gap-3">
            {JURY.map(m => <JuryCard key={m.id} member={m} />)}
          </div>
        </div>
      )}

      {/* Camera */}
      {stage === 'camera' && (
        <div className="fade-in">
          <div className="card p-8">
            <div className="text-center mb-6">
              <div className="emoji-lg mb-2">📸</div>
              <h2 className="text-lg font-semibold text-zinc-800">Show Your Face</h2>
              <p className="text-zinc-500 text-sm">The Skeptic will analyze your expression</p>
            </div>
            
            <div className="webcam-box mb-6">
              <Webcam
                ref={webcamRef}
                audio={false}
                screenshotFormat="image/jpeg"
                videoConstraints={{ facingMode: 'user' }}
                className="w-full block"
              />
            </div>
            
            <button onClick={capture} className="btn btn-primary w-full mb-3">
              Capture Photo
            </button>
            <button onClick={() => { setImage(null); setStage('plea') }} className="btn btn-secondary w-full">
              Skip Photo
            </button>
          </div>
        </div>
      )}

      {/* Plea */}
      {stage === 'plea' && (
        <div className="fade-in">
          <div className="card p-8">
            <div className="text-center mb-6">
              <div className="emoji-lg mb-2">📝</div>
              <h2 className="text-lg font-semibold text-zinc-800">State Your Case</h2>
              <p className="text-zinc-500 text-sm">Make it desperate. The Doctor is listening.</p>
            </div>
            
            {image && (
              <div className="flex justify-center mb-5">
                <img 
                  src={`data:image/jpeg;base64,${image}`}
                  alt="Your face"
                  className="w-24 h-24 rounded-2xl object-cover border-4 border-amber-400 shadow-lg"
                />
              </div>
            )}
            
            <textarea
              value={plea}
              onChange={e => setPlea(e.target.value)}
              placeholder="PLEASE! I've been holding it for 3 hours and I'm about to EXPLODE!!"
              className="h-32 mb-5"
            />
            
            <button onClick={submit} disabled={!plea.trim()} className="btn btn-primary w-full">
              Submit to Court
            </button>
          </div>
        </div>
      )}

      {/* Deliberating */}
      {stage === 'deliberating' && (
        <div className="fade-in text-center">
          <div className="card p-8 mb-8">
            <div className="emoji-lg mb-3">⚖️</div>
            <h2 className="text-lg font-semibold text-purple-600 mb-2">Court is Deliberating</h2>
            <p className="text-zinc-500 text-sm mb-6">The jury is reviewing your case...</p>
            <div className="flex justify-center">
              <div className="spinner"></div>
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-3">
            {JURY.map(m => <JuryCard key={m.id} member={m} loading={true} />)}
          </div>
        </div>
      )}

      {/* Verdict */}
      {stage === 'verdict' && verdict && (
        <div className="fade-in">
          <div className={`card p-8 mb-8 text-center ${
            verdict.verdict === 'GRANTED' ? 'card-granted' : 'card-denied'
          }`}>
            <div className="emoji-xl mb-3">
              {verdict.verdict === 'GRANTED' ? '🎉' : '🚫'}
            </div>
            <h2 className={`text-2xl font-bold mb-2 ${
              verdict.verdict === 'GRANTED' ? 'text-emerald-700' : 'text-red-700'
            }`}>
              {verdict.verdict === 'GRANTED' ? 'Access Granted!' : 'Access Denied'}
            </h2>
            
            <SlotMachine result={verdict.verdict} />
            
            <div className="quote-box text-left my-6">
              <p className="text-xs text-zinc-400 uppercase tracking-wider mb-1">The Pit Boss Says</p>
              <p className="text-zinc-700 italic">"{verdict.roast}"</p>
            </div>
            
            <p className="text-zinc-500 text-sm">{verdict.reasoning}</p>
          </div>
          
          <p className="text-center text-zinc-400 text-xs uppercase tracking-wider mb-4">Jury Votes</p>
          <div className="grid grid-cols-3 gap-3 mb-8">
            {JURY.map(m => (
              <JuryCard 
                key={m.id} 
                member={m} 
                vote={verdict.jury_votes?.[m.id]?.toUpperCase()}
              />
            ))}
          </div>
          
          <button onClick={reset} className="btn btn-primary w-full">
            Try Again
          </button>
        </div>
      )}

      {/* Footer */}
      <footer className="text-center mt-12 text-zinc-400 text-xs">
        Powered by AWS Strands Agents & Claude
      </footer>
    </div>
  )
}
