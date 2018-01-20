// -*- mode:c++ -*-

module comunicacion{

	struct Point {
		int x;
		int y;
	};
	
	interface Coordinacion{
		void RobotDetectado(int angulo, int x, int y, int anchuraScan);
	};


};