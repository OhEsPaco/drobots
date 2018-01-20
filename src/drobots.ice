// -*- mode:c++ -*-

module drobots {

	struct Point {
		int x;
		int y;
	};

	exception NoEnoughEnergy{};

	interface RobotBase {
		void drive(int angle, int speed) throws NoEnoughEnergy;
		short damage() throws NoEnoughEnergy;
		short speed() throws NoEnoughEnergy;
		Point location() throws NoEnoughEnergy;
		short energy() throws NoEnoughEnergy;
	};

	interface Attacker extends RobotBase {
		bool cannon(int angle, int distance) throws NoEnoughEnergy;
	};

	interface Defender extends RobotBase {
		int scan(int angle, int wide) throws NoEnoughEnergy;
	};

	interface Robot extends Attacker, Defender {};

	interface RobotController {
		void turn();
		void robotDestroyed();
		string getTipo();
		Point getPosicionAliado();
	};

	interface RobotControllerDefend extends RobotController {
	};

	interface RobotControllerAttack extends RobotController {
	};

	interface Player {
		RobotController* makeController(Robot* bot);
		void win();
		void lose();
		void gameAbort();
	};

	exception GameInProgress{};
	exception InvalidProxy{};
	exception InvalidName{
		string reason;
	};

	interface Game {
		void login(Player* p, string nick)
			throws GameInProgress, InvalidProxy, InvalidName;
	};

	interface Factory{
		RobotController* make(Robot* robot, int cont1, int cont2);
	};
};
