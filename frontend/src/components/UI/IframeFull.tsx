import Iframe from 'react-iframe';

type Props = {
  url: string;
};

const IframeFull = (props: Props) => {
  const { url } = props;
  return (
    <Iframe
      url={url}
      styles={{
        position: 'absolute',
        width: '90%',
        height: '90%',
        left: '5%',
        right: '5%',
      }}
    ></Iframe>
  );
};

export default IframeFull;
