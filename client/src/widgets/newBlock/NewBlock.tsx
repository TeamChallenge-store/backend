import { useNewProductQuery } from './newBlockApi';
import { ShowMoreProducts } from '~shared/ui/ShowMoreProducts';
import { Loader } from '~shared/ui/Loader';
import { ErrorPopUp } from '~widgets/error-pop-up';


const NewBlock = () => {
  const { data, isLoading } = useNewProductQuery();

  if (isLoading) {
    return <Loader />;
  }

  if (!data) {
    return <ErrorPopUp />;
  }

  const trimmedData = data.slice(0, 8);

  return (
    <div>
      <ShowMoreProducts title="new" products={trimmedData} />
    </div>
  );
};

export { NewBlock };
