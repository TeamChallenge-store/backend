import { Layout } from '~shared/ui/Layout';
import { Header } from '~widgets/header';
import { Search } from '~features/search';
import { Footer } from '~widgets/footer';

const baseLayout = (
  <Layout header={<Header searchSlot={<Search />} />} footer={<Footer />} />
);

export { baseLayout };
