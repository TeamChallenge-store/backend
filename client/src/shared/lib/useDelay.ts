import { useEffect } from 'react';

interface UseDelayProps {
  isShow: boolean;
  hide: () => void;
  delay: number;
}

const useDelay = ({ isShow, hide, delay }: UseDelayProps) => {
  useEffect(() => {
    let timerId: NodeJS.Timeout;

    if (isShow) {
      timerId = setTimeout(() => {
        hide();
      }, delay);
    }

    return () => {
      clearTimeout(timerId);
    };
  }, [hide, isShow, delay]);
};

export default useDelay;
