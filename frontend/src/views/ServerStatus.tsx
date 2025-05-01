import IframeFull from '../components/UI/IframeFull';
import Config from '../config/config';

const ServerStatus = () => {
  return (
    <IframeFull
      url={Config.getInstance().params.grafanaServerStatusUrl}
    ></IframeFull>
  );
};

export default ServerStatus;
