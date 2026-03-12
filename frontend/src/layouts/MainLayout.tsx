import { Outlet } from "react-router-dom";
import NavigationBar from "../components/NavigationBar";
import SideBar from "../components/SideBar";
import '../styles/components.css';

function MainLayout() {
    return (
        <div className="app-container">
            <NavigationBar />
            <main className="page-content">
                <SideBar />
                <Outlet />
            </main>
        </div>
    );
}

export default MainLayout;