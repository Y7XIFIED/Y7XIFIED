export const setMasterVolume = (v: number) => {};
export const getMasterVolume = () => 0;
export const playClick = () => {};
export const playSoftClick = () => {};
export const playKeyTick = () => {};
export const playSuccess = () => {};
export const playPop = () => {};
export const playWhoosh = () => {};
export const playTerminalOpen = () => {};
export const playTerminalClose = () => {};
export const playError = () => {};
export const playHover = () => {};

const useSoundEffects = () => ({
  playClick,
  playSoftClick,
  playKeyTick,
  playSuccess,
  playPop,
  playWhoosh,
  playTerminalOpen,
  playTerminalClose,
  playError,
  playHover,
  setMasterVolume,
  getMasterVolume,
});

export default useSoundEffects;
