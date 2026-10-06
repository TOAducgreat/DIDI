import {Composition} from 'remotion';
import {TrangAn} from './TrangAn';

// 1080x1920 vertical, 30fps, 8 seconds — fits Reels / TikTok / Shorts.
export const RemotionRoot: React.FC = () => (
  <Composition id="TrangAn" component={TrangAn} durationInFrames={240} fps={30} width={1080} height={1920} />
);
