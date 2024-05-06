import { useLocation } from 'react-router-dom';

export const useCheckLocation = () => {
  const location = useLocation();

  const isCheckoutPage = location.pathname === '/checkout';
  const isThankYou = location.pathname === '/thank-you';
  const isError = location.pathname !== '/' && location.key === 'default';

  return { isCheckoutPage, isThankYou, isError };
};
