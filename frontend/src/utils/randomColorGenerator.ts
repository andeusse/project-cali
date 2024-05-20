export const randomColorGenerator = () => {
  return `rgba(${randomByte()}, ${randomByte()}, ${randomByte()}, 0.5)`;
};

const randomByte = () => {
  return Math.random() * 255;
};
