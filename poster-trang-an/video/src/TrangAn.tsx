import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';

const font = `@font-face { font-family: 'PlayfairItalic'; src: url('${staticFile('PlayfairItalic.ttf')}'); }`;

export const TrangAn: React.FC = () => {
  const f = useCurrentFrame();
  const scale = interpolate(f, [0, 240], [1.18, 1.0], {easing: Easing.out(Easing.cubic)});
  const fadeIn = interpolate(f, [0, 30], [0, 1], {extrapolateRight: 'clamp'});
  const textOp = interpolate(f, [150, 190], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const textY = interpolate(f, [150, 190], [30, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: '#0f131c'}}>
      <style>{font}</style>
      <AbsoluteFill style={{opacity: fadeIn, transform: `scale(${scale})`}}>
        <Img src={staticFile('A-dem-ho-guom.png')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 120}}>
        <div style={{opacity: textOp, transform: `translateY(${textY}px)`, fontFamily: 'PlayfairItalic', color: '#c6a670', fontSize: 44}}>
          Lớp 10 Chuyên Sử 1
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
